from rest_framework import serializers

from authentication.models import Client, IdentityProvider


class IdentityProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityProvider
        fields = ['name', 'host', 'api_key', 'app_id']


class ClientSerializer(serializers.ModelSerializer):
    identity_provider = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['name', 'identity_provider', ]

    def get_identity_provider(self, obj):
        return IdentityProviderSerializer(instance=obj.identity_providers.all(), many=True).data
