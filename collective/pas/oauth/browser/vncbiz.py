import json
import urlparse
import urllib

from login import OAuthLogin
from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _
from collective.pas.oauth.interfaces import IOauthVncbizSettings

class VncbizLoginView(OAuthLogin):
    """Vncbiz OAuth 2.0 login view"""

    __provider__ = 'vncbiz'

    def __call__(self):
        super(VncbizLoginView , self).__call__()
        redirect = self.request.response.redirect
        config = self.registry.forInterface(IOauthVncbizSettings)

        verificationCode = self.request.form.get('access_token', None)
        errorReason      = self.request.form.get('error', None)
        redirect_uri = "%s/%s" % (self.context.absolute_url(), self.__name__,)

        args = {
            'client_id': config.client_id, #client_id=11111112-2222222-333333-44444
            'redirect_uri': redirect_uri, #redirect_uri=http://dek4nice.ru/login-vncbiz
            'response_type': 'token', #response_type=token
        }

        if errorReason is not None:
            IStatusMessage(self.request).add(_(u"Vnc.biz authentication denied"), type="error")
            redirect(self.context.absolute_url())
            return u""

        #First request
        if verificationCode is None:
            return self.requestInitial(config.auth_url , args)

        accessToken = verificationCode

        args = {
            'dbname': 'auth_server',
            'access_token': accessToken
        }
        responseProfile = self.requestProfile(config.profile_url , args)

        userId = responseProfile.get('user_id')
        userFullname = responseProfile.get('name')
        # userFullname = userFullname.encode('utf-8')
        userEmail = responseProfile.get('email')

        self.set_token(accessToken)
        self.set_userid(userId)
        self.set_userfullname(userFullname)
        self.set_userlogin(userEmail or userId)
        self.set_useremail(userEmail)

        # # return userFullname
        if self.registration_required:
            args = {
                'form.username' : userId,
                # 'form.fullname' : userFullname,
                'form.email' : userEmail,
            }
            return self.requestJoinForm(args)

        if not userId or not userFullname:
            IStatusMessage(self.request).add(_(u"Insufficient information in Vnc.biz profile"), type="error")
            redirect(self.context.absolute_url())
            return u""

        IStatusMessage(self.request).add(_(u"Welcome. You are now logged in."), type="info")
        redirect(self.context.absolute_url())
