from zope.interface import implements
from zope.component import getUtility

from zope.publisher.interfaces import IPublishTraverse

from Products.Five.browser import BrowserView

from plone.memoize.instance import memoize

from plone.registry.interfaces import IRegistry

from plone.protect import CheckAuthenticator

from collective.pas.oauth import OauthMessageFactory as _
from collective.pas.oauth.interface import IOauthSettings
# from collective.pas.oauth.browser.edit import EditForm
# from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage


class OauthControlPanel(BrowserView):
    """Control panel view
    """

    implements(IPublishTraverse)

    def __call__(self):
        self.cfg_facebook = dict()
        self.update()
        if self.request.response.getStatus() not in (301, 302):
            return self.render()
        return ''

    def update(self):
        self.errors = {}

        self.registry = getUtility(IRegistry)
        self.OauthSettings = self.registry.forInterface(IOauthSettings)

        self.cfg_facebook['client_id']      = self.OauthSettings.facebook_client_id
        self.cfg_facebook['client_secret']  = self.OauthSettings.facebook_client_secret

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

        if self.errors:
            IStatusMessage(self.request).addStatusMessage(_(u"There were errors."), "error")
            return

        self.OauthSettings.facebook_client_id = facebook_client_id
        self.OauthSettings.facebook_client_secret = facebook_client_secret

        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved."), "info")
