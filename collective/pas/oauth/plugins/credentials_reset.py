from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

class CredentialsResetPlugin(BasePlugin):
    """ Callback:  user has logged out.
    """
    security = ClassSecurityInfo()

    security.declarePrivate('resetCredentials')
    def resetCredentials(self, request, response):
        """ Scribble as appropriate.
        """
        #add your code here
        cpo = request.SESSION.get('collective.pas.oauth' , None)
        if cpo is not None:
            request.SESSION.delete('collective.pas.oauth')
        return
