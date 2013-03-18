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

        cpo = request.SESSION.get('collective.pas.oauth' , None)
        if cpo is None:
            return creds
        else:
            return {
                'src'       : self.getId() ,
                'provider'  : cpo.get('userProvider') ,
                'userid'    : cpo.get('userId') ,
                'userfullname'  : cpo.get('userFullname') ,
                'userlogin'  : cpo.get('userLogin') ,
                'useremail' : cpo.get('userEmail') ,
            }

        return creds
