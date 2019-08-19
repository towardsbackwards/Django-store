"""
Github OAuth2 backend, docs at:
    https://python-social-auth.readthedocs.io/en/latest/backends/github.html
"""
from requests import HTTPError

from six.moves.urllib.parse import urljoin

from .oauth import BaseOAuth2
from ..exceptions import AuthFailed


class BaiduOAuth2(BaseOAuth2):
    """Baidu OAuth authentication backend"""
    name = 'baidu'
    API_URL = 'https://openapi.baidu.com/rest/2.0/passport/'
    AUTHORIZATION_URL = 'http://openapi.baidu.com/oauth/2.0/authorize'
    ACCESS_TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
    ACCESS_TOKEN_METHOD = 'GET'
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = False
    STATE_PARAMETER = True
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires'),
        ('login', 'login')
    ]

    def api_url(self):
        return self.API_URL

    def get_user_details(self, response):
        """Return user details from Github account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('realname')
        )
        return {'username': response.get('username'),
                'email': response.get('username'),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        data = self._user_data(access_token)

        return data

    def _user_data(self, access_token, path=None):
        url = urljoin(self.api_url(), 'users/getInfo')
        return self.get_json(url, params={'access_token': access_token})