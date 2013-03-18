
from five.formlib.formbase import PageForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

from plone.app.users.browser.register import RegistrationForm
from Products.CMFCore.utils import getToolByName

class OAuthRegistration(RegistrationForm):
    label = _(u'heading_registration_form', default=u'Registration form')
    description = u""
    template = ViewPageTemplateFile('oauth_register_form.pt')
    sessionkey = 'collective.pas.oauth'

    @property
    def formargs(self):
        regtool = getToolByName(self.context , 'portal_registration')
        password = regtool.generatePassword()
        args = {
            'username'  : self.request.SESSION[self.sessionkey]['userId'],
            'fullname'  : self.request.SESSION[self.sessionkey]['userFullname'],
            'email'     : self.request.SESSION[self.sessionkey]['userEmail'],
            'provider'  : self.request.SESSION[self.sessionkey]['userProvider'],
            'password'  : password,
        }
        return args
