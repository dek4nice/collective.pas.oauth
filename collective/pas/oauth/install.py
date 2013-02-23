from AccessControl.Permissions import manage_users
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService import registerMultiPlugin

import plugin

manage_add_oauth_form = PageTemplateFile('browser/add_plugin',
                            globals(), __name__='manage_add_oauth_form' )


def manage_add_oauth_helper( dispatcher, id, title=None, REQUEST=None ):
    """Add an oauth Helper to the PluggableAuthentication Service."""

    sp = plugin.OauthHelper( id, title )
    dispatcher._setObject( sp.getId(), sp )

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect( '%s/manage_workspace'
                                      '?manage_tabs_message='
                                      'oauthHelper+added.'
                                      % dispatcher.absolute_url() )


def register_oauth_plugin():
    try:
        registerMultiPlugin(plugin.OauthHelper.meta_type)
    except RuntimeError:
        # make refresh users happy
        pass


def register_oauth_plugin_class(context):
    context.registerClass(plugin.OauthHelper,
                          permission = manage_users,
                          constructors = (manage_add_oauth_form,
                                          manage_add_oauth_helper),
                          visibility = None,
                          icon='browser/image_oauth.gif'
                         )
