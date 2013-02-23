"""Class: OauthHelper
"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

import interface
import plugins

class OauthHelper( # -*- implemented plugins -*-
                    plugins.credentials_reset.CredentialsResetPlugin,
                    plugins.authentication.AuthenticationPlugin,
                    plugins.extraction.ExtractionPlugin,
                               ):
    """Multi-plugin

    """

    meta_type = 'Oauth Helper'
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title



classImplements(OauthHelper, interface.IOauthHelper)

InitializeClass( OauthHelper )
