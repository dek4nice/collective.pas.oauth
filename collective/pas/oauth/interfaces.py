from Products.PluggableAuthService import interfaces
from zope.interface import Interface
from zope import schema
from collective.pas.oauth import OauthMessageFactory as _

class IOauthPluginBase(# -*- implemented plugins -*-
                    interfaces.plugins.ICredentialsResetPlugin,
                    interfaces.plugins.IAuthenticationPlugin,
                    interfaces.plugins.IExtractionPlugin,
                                ):
    """interface for OauthPluginBase."""

class IOauthSettings(Interface):
    """OAuth registry settings"""

    registration = schema.Bool(
        title = _(u'registration' , default=u'Register with Plone User'),
        description = _(u'help_registration' , default=u"User will be processed with Plone registration."),
        required = False,
        default = False,
        # readonly = True,
    )

class IOauthGlobalSettings(Interface):
    """OAuth Global registry settings"""

    customprovider_enabled = schema.Bool(
        title = _(u'customprovider_enabled' , default=u'Custom provider'),
        description = _(u'help_customprovider_enabled' , default=u"Authorize with customprovider enabled. This could be your own localhost OAuth2.0 server."),
        required = False,
        default = False,
        # readonly = True,
    )
    facebook_enabled = schema.Bool(
        title = _(u'facebook_enabled' , default=u'Facebook'),
        description = _(u'help_facebook_enabled' , default=u"Authorize with Facebook enabled."),
        required = False,
        default = False,
        # readonly = False,
    )
    vncbiz_enabled = schema.Bool(
        title = _(u'vncbiz_enabled' , default=u'Vnc.biz'),
        description = _(u'help_vncbiz_enabled' , default=u"Authorize with Vnc.biz enabled."),
        required = False,
        default = False,
        # readonly = False,
    )
    google_enabled = schema.Bool(
        title = _(u'google_enabled' , default=u'Google'),
        description = _(u'help_google_enabled' , default=u"Authorize with Google enabled."),
        required = False,
        default = False,
        # readonly = True,
    )
    twitter_enabled = schema.Bool(
        title = _(u'twitter_enabled' , default=u'Twitter'),
        description = _(u'help_twitter_enabled' , default=u"Authorize with Twitter enabled."),
        required = False,
        default = False,
        # readonly = True,
    )
    github_enabled = schema.Bool(
        title = _(u'github_enabled' , default=u'Github'),
        description = _(u'help_github_enabled' , default=u"Authorize with Github enabled."),
        required = False,
        default = False,
        # readonly = True,
    )
    odnoklassniki_enabled = schema.Bool(
        title = _(u'odnoklassniki_enabled' , default=u'Odnoklassniki'),
        description = _(u'help_odnoklassniki_enabled' , default=u"Authorize with Odnoklassniki enabled."),
        required = False,
        default = False,
        # readonly = True,
    )
    vkontakte_enabled = schema.Bool(
        title = _(u'vkontakte_enabled' , default=u'Vkontakte'),
        description = _(u'help_vkontakte_enabled' , default=u"Authorize with Vkontakte enabled."),
        required = False,
        default = False,
        # readonly = True,
    )

class IOauthCustomSettings(Interface):
    """OAuth Custom Provider registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Custom provider client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
        readonly = False,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Custom provider API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
        readonly = False,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Custom provider authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'https://localhost:8080/oauth/authorize',
        readonly = False,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Custom provider access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'https://localhost:8080/oauth/token',
        readonly = False,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Custom provider profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'https://localhost:8080/profile',
        readonly = False,
    )
    post_variable_code = schema.ASCIILine(
        title = _(u'variable_code' , default=u'variable code'),
        description = _(u'help_variable_code' , default=u"?your_variable=code"),
        default = 'code',
        required = False,
    )
    post_redirect_uri = schema.ASCIILine(
        title = _(u'redirect_uri' , default=u'redirect uri'),
        description = _(u'help_redirect_uri' , default=u"?redirect_uri=yourvalue"),
        required = False,
    )
    post_access_token = schema.ASCIILine(
        title = _(u'access_token' , default=u'POST access token'),
        description = _(u'help_access_token' , default=u"?access_token=yourvalue"),
        required = False,
    )
    post_state = schema.ASCIILine(
        title = _(u'state' , default=u'POST state'),
        description = _(u'help_state' , default=u"?state=yourvalue"),
        required = False,
    )



class IOauthVncbizSettings(Interface):
    """OAuth Vncbiz registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Vncbiz client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
        default = '',
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Vncbiz authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'http://demo.vnc.biz:9800/oauth2/auth',
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Vncbiz profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'http://demo.vnc.biz:9800/oauth2/tokeninfo',
    )

class IOauthFacebookSettings(Interface):
    """OAuth Facebook registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Facebook client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
        readonly = False,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Facebook API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
        readonly = False,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Facebook authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'https://graph.facebook.com/oauth/authorize',
        # readonly = True,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Facebook access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'https://graph.facebook.com/oauth/access_token',
        # readonly = True,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Facebook profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'https://graph.facebook.com/me',
        # readonly = True,
    )

class IOauthGoogleSettings(Interface):
    """OAuth Google registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Google client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Google API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Google authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'https://accounts.google.com/o/oauth2/auth',
        # readonly = True,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Google access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'https://accounts.google.com/o/oauth2/token',
        # readonly = True,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Google profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

class IOauthTwitterSettings(Interface):
    """OAuth Twitter registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Twitter client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Twitter API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Twitter authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Twitter access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Twitter profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

class IOauthGithubSettings(Interface):
    """OAuth Github registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Github client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Github API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Github authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'https://github.com/login/oauth/authorize',
        # readonly = True,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Github access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'https://github.com/login/oauth/access_token',
        # readonly = True,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Github profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

class IOauthOdnoklassnikiSettings(Interface):
    """OAuth Odnoklassniki registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Odnoklassniki client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Odnoklassniki API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Odnoklassniki authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Odnoklassniki access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Odnoklassniki profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

class IOauthVkontakteSettings(Interface):
    """OAuth Vkontakte registry settings"""

    client_id = schema.ASCIILine(
        title = _(u'client_id' , default=u'Vkontakte client ID'),
        description = _(u'help_client_id' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    client_secret = schema.ASCIILine(
        title = _(u'client_secret' , default=u'Vkontakte API Secret'),
        description = _(u'help_client_secret' , default=u"Alternatively, you can of course use the ID of an existing app."),
        required = True,
    )

    auth_url = schema.URI(
        title = _(u'auth_url' , default=u'Vkontakte authorize url'),
        description = _(u'help_auth_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

    token_url = schema.URI(
        title = _(u'token_url' , default=u'Vkontakte access token url'),
        description = _(u'help_token_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

    profile_url = schema.URI(
        title = _(u'profile_url' , default=u'Vkontakte profile url'),
        description = _(u'help_profile_url' , default=u""),
        required = True,
        default = 'http://localhost:8080/',
        # readonly = True,
    )

