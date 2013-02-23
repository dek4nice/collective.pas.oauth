Tests for collective.pas.oauth

test setup
----------

    >>> from Testing.ZopeTestCase import user_password
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()

Plugin setup
------------

    >>> acl_users_url = "%s/acl_users" % self.portal.absolute_url()
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % ('portal_owner', user_password))
    >>> browser.open("%s/manage_main" % acl_users_url)
    >>> browser.url
    'http://nohost/plone/acl_users/manage_main'
    >>> form = browser.getForm(index=0)
    >>> select = form.getControl(name=':action')

collective.pas.oauth should be in the list of installable plugins:

    >>> 'Oauth Helper' in select.displayOptions
    True

and we can select it:

    >>> select.getControl('Oauth Helper').click()
    >>> select.displayValue
    ['Oauth Helper']
    >>> select.value
    ['manage_addProduct/collective.pas.oauth/manage_add_oauth_helper_form']

we add 'Oauth Helper' to acl_users:

    >>> from collective.pas.oauth.plugin import OauthHelper
    >>> myhelper = OauthHelper('myplugin', 'Oauth Helper')
    >>> self.portal.acl_users['myplugin'] = myhelper

and so on. Continue your tests here

    >>> 'ALL OK'
    'ALL OK'

