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

        args = {
            'client_id': config.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'token',
        }

        if errorReason is not None:
            IStatusMessage(self.request).add(_(u"Vnc.biz authentication denied"), type="error")
            redirect(self.context.absolute_url())
            return u""

        #First request
        if verificationCode is None:
            return self.requestInitial(config.auth_url , args)

        accessToken = verificationCode

        #profile section
        args = {
            'dbname': 'auth_server',
            'access_token': accessToken
        }
        responseProfile = self.requestProfile(config.profile_url , args)
        userId       = responseProfile.get('user_id', '')
        userFullname = responseProfile.get('name' , '')
        userEmail    = responseProfile.get('email')

        if not userId or not userEmail:
            IStatusMessage(self.request).add(_(u"Insufficient information in Vnc.biz profile"), type="error")
            redirect(self.context.absolute_url())
            return u""

        self.set_token(accessToken)
        self.set_user_data(userId=userId , userEmail=userEmail , userFullname=userFullname)

        if self.registration_required:
            # args = {'form.username':userId, 'form.fullname':userFullname, 'form.email':userEmail,}
            return self.requestJoinForm()

        IStatusMessage(self.request).add(_(u"Welcome. You are now logged in."), type="info")
        redirect(self.context.absolute_url())
