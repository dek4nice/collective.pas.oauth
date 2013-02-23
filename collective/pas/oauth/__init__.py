from zope.i18nmessageid import MessageFactory
OauthMessageFactory = MessageFactory('collective.pas.oauth')

import install

install.register_oauth_plugin()

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    install.register_oauth_plugin_class(context)
