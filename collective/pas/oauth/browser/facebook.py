import json
import urlparse
import urllib

from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _

from login import OAuthLogin
from login import config
# import pdb
class FacebookLoginView(OAuthLogin):
    """Facebook OAuth 2.0 login view"""

    def __call__(self):
        redirect = self.request.response.redirect
        verificationCode = self.request.form.get("code", None)
        errorReason      = self.request.form.get("error_reason", None)
        
        args = {
                'client_id': config.facebook_client_id,
                'redirect_uri': "%s/%s" % (self.context.absolute_url(), self.__name__,),
            }
        
        # Did we get an error back after a Facebook redirect?

        if errorReason is not None:
            IStatusMessage(self.request).add(_(u"Facebook authentication denied"), type="error")
            redirect(self.context.absolute_url())
            return u""
        
        # If there is no code, this is probably the first request, so redirect
        # to Facebook
        
        if verificationCode is None:
            redirect_uri  = "%s?%s" % (config.facebook_auth_url , urllib.urlencode(args),)
            redirect(redirect_uri)
            return u""

        # If we are on the return path form Facebook, exchange the return code
        # for a token

        args["client_secret"] = config.facebook_client_secret
        args["code"] = verificationCode

        redirect_uri = "%s?%s" % (config.facebook_access_token_url , urllib.urlencode(args),)
        # pdb.set_trace()
        response = urlparse.parse_qs(urllib.urlopen(redirect_uri).read())
        # return [response]
        # Load the profile using the access token we just received
        accessToken = response["access_token"][-1]
        args_profile = {'access_token': accessToken , 'fields': 'id,email,name'}
        redirect_uri = "%s?%s" % (config.facebook_profile_url , urllib.urlencode(args_profile),)
        profile = json.load(urllib.urlopen(redirect_uri))

        userId = profile.get('id')
        userFullname = profile.get('name')
        userEmail = profile.get('email')

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
