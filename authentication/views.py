from django.conf import settings
from django.utils import timezone

from rest_framework.response import Response
from rest_framework import generics

class StatusCheckView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        title = u'TCC SSO API'
        full_title = '{} (v{}- {})'.format(
            title,
            getattr(settings, 'CENTURION_VERSION', '0.0.1'),
            getattr(settings, 'CENTURION_ENVIRONMENT', 'prod').upper(),
        )
        now = timezone.localtime(timezone.now())
        print('-' * 50)
        print(full_title)
        print('Hora do servidor', now)
        print('SSO NIAS TECNOLOGIA')
        print('-' * 50)
        return Response({'status': 'OK'}, status=200)