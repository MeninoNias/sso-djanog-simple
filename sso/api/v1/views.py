from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.auth import ClientUserAuthentication
from authentication.models import Client


class LoginAPIView(APIView):
    authentication_classes = (ClientUserAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        client = request.user.clientUser
        identity_provider = client.identity_providers.order_by('?').first()

        username = request.data.get('email')
        password = request.data.get('password')

        print('username', username)
        print('password', password)

        response = identity_provider.connection(username, password)
        if response.status_code == 200:
            print("-------------------------------------")
            # print("Sucesso! O usuário foi autenticado.")
            print(response.json())
            print("-------------------------------------")
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # print(response.__dict__)
            print("Erro ao autenticar o usuário. Status code:", response.status_code)
            print(response.json())
        return Response({'message': 'ERROR'}, status=response.status_code)

        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        # else:
        #     return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
