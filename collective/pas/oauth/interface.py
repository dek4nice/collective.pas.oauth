from Products.PluggableAuthService import interfaces
from zope.interface import Interface
from zope import schema
from collective.pas.oauth import OauthMessageFactory as _

class IOauthHelper(# -*- implemented plugins -*-
                    interfaces.plugins.ICredentialsResetPlugin,
                    interfaces.plugins.IAuthenticationPlugin,
                    interfaces.plugins.IExtractionPlugin,
                                ):
    """interface for OauthHelper."""

class IOauthSettings(Interface):
    """OAuth registry settings"""

    facebook_client_id = schema.ASCIILine(
        title = _(u'facebook_client_id' , default=u'Facebook client ID'),
        description = _(u'help_facebook_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = False,
    )
    facebook_client_secret = schema.ASCIILine(
        title = _(u'facebook_client_secret' , default=u'Facebook API Secret'),
        description = _(u'help_facebook_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = False,
    )

