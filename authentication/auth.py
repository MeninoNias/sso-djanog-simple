from django.contrib.auth.models import AnonymousUser

from rest_framework import authentication
from rest_framework import exceptions

from authentication.models import Client


class ClientUser(AnonymousUser):

    def __init__(self, clientUser):
        self.clientUser = clientUser

    def __str__(self):
        return 'Client User: ' + str(self.clientUser)

    @property
    def is_authenticated(self):
        return True


class ClientUserAuthentication(authentication.BasicAuthentication):
    def authenticate_credentials(self, userid, password, request=None):
        try:
            clientUser = Client.objects.get(pk=userid, api_key=password)
        except:
            raise exceptions.AuthenticationFailed()

        return (ClientUser(clientUser), None)
