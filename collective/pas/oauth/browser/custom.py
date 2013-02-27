import json
import urlparse
import urllib

from login import OAuthLogin
from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _
from collective.pas.oauth.interfaces import IOauthCustomSettings

class CustomLoginView(OAuthLogin):
    """Custom OAuth 2.0 login view"""

    def __call__(self):
        super(CustomLoginView , self).__call__()
        redirect = self.request.response.redirect
        verificationCode = self.request.form.get("code", None)
        errorReason      = self.request.form.get("error", None)

        redirect_uri = "%s/%s" % (self.context.absolute_url(), self.__name__,)

        config = self.registry.forInterface(IOauthCustomSettings)

        args = {
            'client_id': config.client_id,
            'redirect_uri': redirect_uri,
        }

        if errorReason is not None:
            IStatusMessage(self.request).add(_(u"Custom authentication denied"), type="error")
            redirect(self.context.absolute_url())
            return u""

        #First request
        if verificationCode is None:
            return self.requestInitial(config.auth_url , args)

        return 'asd'
        args["client_secret"] = config.client_secret
        args["code"] = verificationCode

        responseToken = self.requestToken(config.token_url , args)
        accessToken = responseToken["access_token"][-1]

        args = {
            'access_token': accessToken ,
            'fields': 'id,email,name',
        }
        responseProfile = self.requestProfile(config.profile_url , args)

        # return responseProfile

        userId = responseProfile.get('id')
        userFullname = responseProfile.get('name')
        userFullname = userFullname.encode('utf-8')
        userEmail = responseProfile.get('email')

        self.set_token(accessToken)
        self.set_userid(userId)
        self.set_userfullname(userFullname)
        self.set_userlogin(userEmail or userId)
        self.set_useremail(userEmail)

        # return userFullname
        if self.registration_required:
            args = {
                'form.username' : userId,
                'form.fullname' : userFullname,
                'form.email' : userEmail,
            }
            return self.requestJoinForm(args)

        if not userId or not userFullname:
            IStatusMessage(self.request).add(_(u"Insufficient information in Custom profile"), type="error")
            redirect(self.context.absolute_url())
            return u""

        IStatusMessage(self.request).add(_(u"Welcome. You are now logged in."), type="info")
        redirect(self.context.absolute_url())

    @property
    def checkin_enabled(self):
        return self.checkin_provider_enabled('customprovider')
