from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.api.v1.serializers import ClientSerializer
from authentication.auth import ClientUserAuthentication
from authentication.models import Client


class ClientAPIView(APIView):
    authentication_classes = (ClientUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(pk=self.request.user.clientUser.pk)

    def get_object(self):
        return self.get_queryset().first()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)
