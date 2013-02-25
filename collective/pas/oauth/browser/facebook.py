import json
import urlparse
import urllib

from login import OAuthLogin
from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.pas.oauth.interfaces import IOauthFacebookSettings

class FacebookLoginView(OAuthLogin):
    """Facebook OAuth 2.0 login view"""

    def __call__(self):
        redirect = self.request.response.redirect
        verificationCode = self.request.form.get("code", None)
        errorReason      = self.request.form.get("error_reason", None)

        redirect_uri = "%s/%s" % (self.context.absolute_url(), self.__name__,)

        registry = getUtility(IRegistry)
        cfg_facebook = registry.forInterface(IOauthFacebookSettings)

        args = {
            'client_id': cfg_facebook.client_id,
            'redirect_uri': redirect_uri,
        }

        if errorReason is not None:
            IStatusMessage(self.request).add(_(u"Facebook authentication denied"), type="error")
            redirect(self.context.absolute_url())
            return u""

        #First request
        if verificationCode is None:
            return self.requestInitial(cfg_facebook.auth_url , args)

        args["client_secret"] = cfg_facebook.client_secret
        args["code"] = verificationCode

        responseToken = self.requestToken(cfg_facebook.token_url , args)
        accessToken = responseToken["access_token"][-1]

        args_profile = {'access_token': accessToken , 'fields': 'id,email,name'}
        responseProfile = self.requestProfile(cfg_facebook.profile_url , args_profile)

        userId = responseProfile.get('id')
        userFullname = responseProfile.get('name')
        userEmail = responseProfile.get('email')

        self.set_token(accessToken)
        self.set_userid(userId)
        self.set_userfullname(userFullname)
        self.set_userlogin(userEmail or userId)
        self.set_useremail(userEmail)

        if not userId or not userFullname:
            IStatusMessage(self.request).add(_(u"Insufficient information in Facebook profile"), type="error")
            redirect(self.context.absolute_url())
            return u""

        IStatusMessage(self.request).add(_(u"Welcome. You are now logged in."), type="info")
        redirect(self.context.absolute_url())

    def checkin_enabled(self):
        # python:member is None and path('object/@@login-facebook').checkin_enabled()
        return super(OAuthLogin, self).checkin_enabled('facebook')
