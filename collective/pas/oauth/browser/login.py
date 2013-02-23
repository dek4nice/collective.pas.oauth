import json
import urlparse
import urllib

from zope.publisher.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _

from collective.pas.oauth.browser import config

class OAuthLogin(BrowserView):
    """OAuth 2.0 base"""
    sessionkey = 'collective.pas.oauth'

    def __call__(self):
        return

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
