import requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.auth import ClientUserAuthentication
from authentication.models import UserIdentity
from sso.models import AccessIdentity


class LoginAPIView(APIView):
    authentication_classes = (ClientUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        client = request.user.clientUser
        identity_provider = client.identity_providers.order_by('?').first()

        username = request.data.get('email')
        password = request.data.get('password')

        access_identity = AccessIdentity(provider=identity_provider)

        try:
            response = identity_provider.connection(username, password)
            if response.status_code == 200:
                data = response.json()
                access_identity.status_code = response.status_code
                access_identity.data = data
                access_identity.save()

                idd, unused = UserIdentity.objects.get_or_create(
                    provider=identity_provider,
                    external_id=data['user']['id']
                )
                idd.token = data['token']
                idd.name = data['user']['name']
                idd.username = data['user']['email']
                idd.email = data['user']['email']
                idd.save()

                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        except requests.exceptions.Timeout:
            access_identity.status_code = status.HTTP_408_REQUEST_TIMEOUT
            access_identity.data = 'ERROR - PROVEDOR DE INFORMAÇÕES TIME OUT'
            access_identity.save()
            return Response({'message': 'ERROR - PROVEDOR DE INFORMAÇÕES'}, status=status.HTTP_204_NO_CONTENT)

        access_identity.status_code = response.status_code
        access_identity.data = response.json()
        access_identity.save()

        return Response({'message': 'ERROR'}, status=response.status_code)
