from urllib import request

from jose import jwt
from social_core.backends.auth0 import Auth0OAuth2


class Auth0(Auth0OAuth2):
    def get_user_details(self, response):
        # Obtain JWT and the keys to validate the signature
        id_token = response.get('id_token')
        jwks = request.urlopen('https://' + self.setting('DOMAIN') + '/.well-known/jwks.json')
        issuer = 'https://' + self.setting('DOMAIN') + '/'
        audience = self.setting('KEY')  # CLIENT_ID
        payload = jwt.decode(id_token, jwks.read(), algorithms=['RS256'], audience=audience, issuer=issuer)

        return {
            'username': payload['nickname'],
            'first_name': payload['name'],
            'picture': payload['picture'],
            'user_id': payload['sub'],
            'role': payload['https://imdb-django/role'],
        }
