import json
import urlparse
import urllib

from zope.publisher.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.pas.oauth.interfaces import IOauthSettings
from collective.pas.oauth.interfaces import IOauthGlobalSettings

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

class OAuthLogin(BrowserView):
    """OAuth 2.0 base"""
    sessionkey = 'collective.pas.oauth'

    def __call__(self):
        self.portal = getUtility(ISiteRoot)
        self.registry = getUtility(IRegistry)
        self.config_base = self.registry.forInterface(IOauthSettings)
        self.config_global = self.registry.forInterface(IOauthGlobalSettings)
        self.redirect_uri = "%s/%s" % (self.context.absolute_url(), self.__name__,)

        if self.sessionkey not in self.request.SESSION.keys():
            self.request.SESSION[self.sessionkey] = {}
        return


    def requestInitial(self, request_url, args):
        redirect_uri  = "%s?%s" % (request_url , urllib.urlencode(args),)
        self.request.response.redirect(redirect_uri)
        return

    def requestToken(self, request_url, args):
        redirect_uri = "%s?%s" % (request_url , urllib.urlencode(args),)
        # {"error":{"message":"This authorization code has expired.","type":"OAuthException","code":100}}
        # access_token=AAAB3Tt56fioBAOm3APZBiCGRWKnPRnmfIGrUhQ8Rs2WVRnRjsocSgBpOFaQTg7AXJDZBBK8VZBnmJQXNUKFA0ETW2XsHa47sqxuL3VQfgZDZD&expires=5179564
        return urlparse.parse_qs(urllib.urlopen(redirect_uri).read())

    def requestProfile(self, request_url, args):
        redirect_uri = "%s?%s" % (request_url , urllib.urlencode(args),)
        return json.load(urllib.urlopen(redirect_uri))

    def requestJoinForm(self):
        email = self.request.SESSION[self.sessionkey]['userEmail']
        if self.check_user_created(email):
            IStatusMessage(self.request).add(_(u"Welcome. You are now logged in."), type="info")
            template = ''
            # args = {'__ac_name' : email,}
            # template = 'login_form'
        else:
            template = "@@login-register"
        redirect_uri = "%s/%s" % (self.context.absolute_url() , template)
        self.request.response.redirect(redirect_uri)
        return

    def check_user_created(self , userId):
        mt = getToolByName(self.context, 'portal_membership')
        return mt.getMemberById(userId)

    def set_token(self, accessToken):
        self.request.SESSION[self.sessionkey]['accessToken'] = accessToken

    def set_user_data(self, userId, userEmail, userFullname='', userLogin=''):
        self.request.SESSION[self.sessionkey]['userId'] = userId
        self.request.SESSION[self.sessionkey]['userEmail'] = userEmail
        self.request.SESSION[self.sessionkey]['userFullname'] = userFullname
        if not userFullname:
            userFullname = userId
        if not userLogin:
            userLogin = userEmail or userId
        self.request.SESSION[self.sessionkey]['userLogin'] = userLogin
        self.request.SESSION[self.sessionkey]['userProvider'] = self.__provider__

    @property
    def registration_required(self):
        return getattr(self.config_base , 'registration')

    def checkin_show_login_tab(self):
        mt = getToolByName(self.context, 'portal_membership')
        if not mt.isAnonymousUser():
            return False
        else:
            if self.checkin_provider_enabled(self.__provider__):
                return True

    def checkin_provider_enabled(self, property):
        # python:member is None and path('object/@@login-twitter').checkin_enabled()
        #python:member is None
        registry = getUtility(IRegistry)
        config_global = registry.forInterface(IOauthGlobalSettings)
        return getattr(config_global , property + '_enabled')
