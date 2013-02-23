import json
import urlparse
import urllib

from Products.statusmessages.interfaces import IStatusMessage
from collective.pas.oauth import OauthMessageFactory as _

from login import OAuthLogin
from login import config

class TwitterLoginView(OAuthLogin):
    """Twitter OAuth 2.0 login view"""

    def __call__(self):
        verificationCode = self.request.form.get("code", None)
        errorReason      = self.request.form.get("error_reason", None)
        raise Exception('Twitter not avaliable at the moment')
