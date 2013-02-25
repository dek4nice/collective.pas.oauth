import json
import urlparse
import urllib

from zope.publisher.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.pas.oauth.interfaces import IOauthGlobalSettings

class OAuthLogin(BrowserView):
    """OAuth 2.0 base"""
    sessionkey = 'collective.pas.oauth'

    def __call__(self):
        return

    def requestInitial(self, request_url, args):
        redirect_uri  = "%s?%s" % (request_url , urllib.urlencode(args),)
        self.request.response.redirect(redirect_uri)
        return

    def requestToken(self, request_url, args):
        redirect_uri = "%s?%s" % (request_url , urllib.urlencode(args),)
        return urlparse.parse_qs(urllib.urlopen(redirect_uri).read())

    def requestProfile(self, request_url, args):
        redirect_uri = "%s?%s" % (request_url , urllib.urlencode(args),)
        return json.load(urllib.urlopen(redirect_uri))

    def check_user_created(self):
        pass

    def set_session(self):
        if self.sessionkey not in self.request.SESSION.keys():
            self.request.SESSION[self.sessionkey] = {}

    def set_token(self, accessToken):
        self.set_session()
        self.request.SESSION[self.sessionkey]['accessToken'] = accessToken

    def set_userid(self, userId):
        self.set_session()
        self.request.SESSION[self.sessionkey]['userId'] = userId

    def set_userlogin(self, userLogin):
        self.set_session()
        self.request.SESSION[self.sessionkey]['userLogin'] = userLogin

    def set_userfullname(self, userFullname):
        self.set_session()
        self.request.SESSION[self.sessionkey]['userFullname'] = userFullname

    def set_useremail(self, userEmail):
        self.set_session()
        self.request.SESSION[self.sessionkey]['userEmail'] = userEmail

    def checkin_enabled(self, property):
        registry = getUtility(IRegistry)
        cfg_global = registry.forInterface(IOauthGlobalSettings)
        return getattr(cfg_global , property + '_enabled')
