from StringIO import StringIO
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from collective.pas.oauth.plugin import OauthPluginBase

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.pas.oauth.interfaces import IOauthGlobalSettings
from collective.pas.oauth.interfaces import IOauthCustomSettings
from collective.pas.oauth.interfaces import IOauthFacebookSettings
from collective.pas.oauth.interfaces import IOauthGoogleSettings
from collective.pas.oauth.interfaces import IOauthTwitterSettings
from collective.pas.oauth.interfaces import IOauthGithubSettings
from collective.pas.oauth.interfaces import IOauthOdnoklassnikiSettings
from collective.pas.oauth.interfaces import IOauthVkontakteSettings

def update_registry():
    registry = getUtility(IRegistry)
    registry.registerInterface(IOauthGlobalSettings)
    registry.registerInterface(IOauthCustomSettings)
    registry.registerInterface(IOauthFacebookSettings)
    registry.registerInterface(IOauthGoogleSettings)
    registry.registerInterface(IOauthTwitterSettings)
    registry.registerInterface(IOauthGithubSettings)
    registry.registerInterface(IOauthOdnoklassnikiSettings)
    registry.registerInterface(IOauthVkontakteSettings)

def install_plugin(portal, name='collective-pas-oauth'):
    out = StringIO()
    userFolder = portal['acl_users']
    
    if name not in userFolder:
        plugin = OauthPluginBase(name, 'Oauth Plugin Base')
        userFolder[name] = plugin

        activatePluginInterfaces(portal, name, out)

        # Move plugin to the top of the list for each active interface
        plugins = userFolder['plugins']
        for info in plugins.listPluginTypeInfo():
            interface = info['interface']
            if plugin.testImplements(interface):
                active = list(plugins.listPluginIds(interface))
                if name in active:
                    active.remove(name)
                    active.insert(0, name)
                    plugins._plugins[interface] = tuple(active)
        
        return out.getvalue()

def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('collective.pas.oauth.txt') is None:
        return
    portal = context.getSite()

    update_registry()
    install_plugin(portal)

