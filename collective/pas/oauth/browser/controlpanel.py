from zope.interface import implements
from zope.component import getUtility

from zope.publisher.interfaces import IPublishTraverse

from Products.Five.browser import BrowserView

from plone.memoize.instance import memoize

from plone.protect import CheckAuthenticator

from collective.pas.oauth import OauthMessageFactory as _
from plone.registry.interfaces import IRegistry
from collective.pas.oauth.interfaces import IOauthSettings
from collective.pas.oauth.interfaces import IOauthGlobalSettings
from collective.pas.oauth.interfaces import IOauthCustomSettings
from collective.pas.oauth.interfaces import IOauthVncbizSettings
from collective.pas.oauth.interfaces import IOauthFacebookSettings
from collective.pas.oauth.interfaces import IOauthGoogleSettings
from collective.pas.oauth.interfaces import IOauthTwitterSettings
from collective.pas.oauth.interfaces import IOauthGithubSettings
from collective.pas.oauth.interfaces import IOauthOdnoklassnikiSettings
from collective.pas.oauth.interfaces import IOauthVkontakteSettings
# from collective.pas.oauth.browser.edit import EditForm
# from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage

class OauthFieldset(object):
    """Base provider class"""

    def __init__(self, id, interface, title='', description='', provider=False):
        registry = getUtility(IRegistry)

        self.id = id
        self.__name__ = self.id
        self.__interface = interface
        self.__config = registry.forInterface(self.__interface, check=False)
        self.__fields__ = self.__interface._InterfaceClass__attrs
        for f in self.__fields__:
            self.__fields__[f].id = self.__fields__[f].__name__
            self.__fields__[f].request_id = self.__name__ + '_' + self.__fields__[f].__name__
            self.__fields__[f].registry_value = getattr(self.__config , f)
        self.__title = title or id or ''
        self.__description = description or ''
        self.is_provider = bool(provider)

    def field_value(self, field_id):
        return getattr(self.__config , field_id)

    # @property
    def description(self):
        return self.__description

    # @property
    def title(self):
        return self.__title

    # @property
    def fields(self):
        return self.__fields__.values()

    def save_settings(self , form):
        for field in self.fields():
            request_value = form.get(field.request_id , None)
            if request_value is None:
                continue
            elif request_value == field.registry_value:
                continue
            else:
                setattr(self.__config , field.id , request_value)

class OauthControlPanel(BrowserView):
    """Control panel view
    """

    implements(IPublishTraverse)

    providers_list = {
        'customprovider' : IOauthCustomSettings,
        'vncbiz' : IOauthVncbizSettings,
        'facebook' : IOauthFacebookSettings,
        'google' : IOauthGoogleSettings,
        'twitter' : IOauthTwitterSettings,
        'github' : IOauthGithubSettings,
        'odnoklassniki' : IOauthOdnoklassnikiSettings,
        'vkontakte' : IOauthVkontakteSettings,
    }

    def __call__(self):
        registry = getUtility(IRegistry)

        self.__fieldsets__ = list()

        self.__fieldsets__.append(OauthFieldset('base' , IOauthSettings , 'Base settings'))
        self.fieldset_global = OauthFieldset('global' , IOauthGlobalSettings , title='Public providers' , description='Enable/disable required services')
        self.__fieldsets__.append(self.fieldset_global)

        for provider_id in self.providers_list:
            provider_interface = self.providers_list[provider_id]
            provider_field = self.fieldset_global.__fields__[provider_id + '_enabled']
            self.__fieldsets__.append(OauthFieldset(provider_id , provider_interface , title=provider_field.title , description=provider_field.description , provider=True))

        self.update()
        if self.request.response.getStatus() not in (301, 302):
            return self.render()
        return ''

    def provider_enabled(self , provider_id):
        return self.fieldset_global.field_value(provider_id + '_enabled')

    @property
    def fieldsets(self):
        return self.__fieldsets__

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

        for fieldset in self.__fieldsets__:
            fieldset.save_settings(form)

        if self.errors:
            IStatusMessage(self.request).addStatusMessage(_(u"There were errors."), "error")
            return

        # self.cfg_facebook.auth_url = facebook_auth_url

        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."), "info")
