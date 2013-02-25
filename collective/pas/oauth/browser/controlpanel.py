from zope.interface import implements
from zope.component import getUtility

from zope.publisher.interfaces import IPublishTraverse

from Products.Five.browser import BrowserView

from plone.memoize.instance import memoize

from plone.protect import CheckAuthenticator

from collective.pas.oauth import OauthMessageFactory as _
from plone.registry.interfaces import IRegistry
from collective.pas.oauth.interfaces import IOauthGlobalSettings
from collective.pas.oauth.interfaces import IOauthCustomSettings
from collective.pas.oauth.interfaces import IOauthFacebookSettings
from collective.pas.oauth.interfaces import IOauthGoogleSettings
from collective.pas.oauth.interfaces import IOauthTwitterSettings
from collective.pas.oauth.interfaces import IOauthGithubSettings
from collective.pas.oauth.interfaces import IOauthOdnoklassnikiSettings
from collective.pas.oauth.interfaces import IOauthVkontakteSettings
# from collective.pas.oauth.browser.edit import EditForm
# from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage


class OauthControlPanel(BrowserView):
    """Control panel view
    """

    implements(IPublishTraverse)

    def __call__(self):
        registry = getUtility(IRegistry)

        self.fields_keys = ['global','customprovider','facebook','google','twitter','github','odnoklassniki','vkontakte']
        self.fields = dict()
        # self.fields['global']           = IOauthGlobalSettings._InterfaceClass__attrs
        self.fields['customprovider']   = IOauthCustomSettings._InterfaceClass__attrs
        self.fields['facebook']         = IOauthFacebookSettings._InterfaceClass__attrs
        self.fields['google']           = IOauthGoogleSettings._InterfaceClass__attrs
        self.fields['twitter']          = IOauthTwitterSettings._InterfaceClass__attrs
        self.fields['github']           = IOauthGithubSettings._InterfaceClass__attrs
        self.fields['odnoklassniki']    = IOauthOdnoklassnikiSettings._InterfaceClass__attrs
        self.fields['vkontakte']        = IOauthVkontakteSettings._InterfaceClass__attrs
        self.fields_global              = IOauthGlobalSettings._InterfaceClass__attrs

        self.cfg_global         = registry.forInterface(IOauthGlobalSettings, check=False)
        self.cfg_customprovider = registry.forInterface(IOauthCustomSettings, check=False)
        self.cfg_facebook       = registry.forInterface(IOauthFacebookSettings, check=False)
        self.cfg_google         = registry.forInterface(IOauthGoogleSettings, check=False)
        self.cfg_twitter        = registry.forInterface(IOauthTwitterSettings, check=False)
        self.cfg_github         = registry.forInterface(IOauthGithubSettings, check=False)
        self.cfg_odnoklassniki  = registry.forInterface(IOauthOdnoklassnikiSettings, check=False)
        self.cfg_vkontakte      = registry.forInterface(IOauthVkontakteSettings, check=False)

        self.update()
        if self.request.response.getStatus() not in (301, 302):
            return self.render()
        return ''

    def update(self):
        self.errors = {}

        if self.request.method == 'POST':
            CheckAuthenticator(self.request)
            if 'form.button.Save' in self.request.form:
                self.processSave()
            elif 'form.button.Cancel' in self.request.form:
                self.request.response.redirect("%s/plone_control_panel" % self.context.absolute_url())

    def render(self):
        return self.index()

    def processSave(self):
        form = self.request.form

        facebook_client_id       = form.get('facebook_client_id', False)
        facebook_client_secret   = form.get('facebook_client_secret', False)
        facebook_auth_url        = form.get('facebook_auth_url', False)

        if self.errors:
            IStatusMessage(self.request).addStatusMessage(_(u"There were errors."), "error")
            return

        self.cfg_facebook.client_id = facebook_client_id
        self.cfg_facebook.client_secret = facebook_client_secret
        self.cfg_facebook.auth_url = facebook_auth_url

        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."), "info")
