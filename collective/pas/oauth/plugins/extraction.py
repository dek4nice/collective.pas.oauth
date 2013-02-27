from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin

class ExtractionPlugin(BasePlugin):
    """ Extracts login name and credentials from a request.
    """
    security = ClassSecurityInfo()

    security.declarePrivate('extractCredentials')
    def extractCredentials(self, request):

        """ request -> {...}

        o Return a mapping of any derived credentials.

        o Return an empty mapping to indicate that the plugin found no
          appropriate credentials.
        """
        creds = {}

        #add your code here
        # self.testf()
        cpo = request.SESSION.get('collective.pas.oauth' , None)
        if cpo is None:
            return creds
        else:
            return {
                'src'       : self.getId() ,
                'userid'    : cpo['userId'] ,
                'userlogin'  : cpo['userLogin'] ,
                'useremail' : cpo['userEmail'] ,
            }

        return creds
