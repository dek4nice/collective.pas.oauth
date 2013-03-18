from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.pas.oauth.interfaces import IOauthSettings
from Products.CMFCore.utils import getToolByName

import logging
logger = logging.getLogger("collective.pas.oauth")

class AuthenticationPlugin(BasePlugin):
    """ Map credentials to a user ID.
    """
    security = ClassSecurityInfo()

    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):

        """ credentials -> (userid, login)

        o 'credentials' will be a mapping, as returned by IExtractionPlugin.

        o Return a  tuple consisting of user ID (which may be different
          from the login name) and login

        o If the credentials cannot be authenticated, return None.
        """
        user_id = ''
        user_login = ''

        if credentials.get('src', None) != self.getId():
            return
        if ('userid' in credentials and 'userlogin' in credentials):
            registry = getUtility(IRegistry)
            config_base = registry.forInterface(IOauthSettings)
            if config_base.registration:
                mtool = getToolByName(self, 'portal_membership')
                user = mtool.getMemberById(credentials['useremail'])
                if user:
                    user_id = login = user.getId()
                    self._getPAS().updateCredentials(self.REQUEST, self.REQUEST.RESPONSE, login, "")
                    return (user_id, login)
                else:
                    return
            else:
                return (credentials['useremail'] , credentials['useremail'])
        else:
            return None

        raise Exception('Credentials:',credentials)
        return (user_id, user_login)
