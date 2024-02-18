from django.contrib import admin
from django.contrib.auth.models import Group

from authentication.models import Client, IdentityProvider, UserIdentity

admin.site.unregister(Group)


def hard_delete(modeladmin, request, obj):
    obj.hard_delete()


class BaseAdmin(admin.ModelAdmin):
    queryset_class = None
    actions = [hard_delete]
    ordering = ('-created_at',)
    list_filter = ['is_active']

    def get_queryset(self, request):
        return self.queryset_class.all_objects.all()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ()


@admin.register(Client)
class ClientAdmin(BaseAdmin):
    queryset_class = Client
    list_display = ['name', 'app_id', 'api_key', 'created_at', 'updated_at',]
    ordering = ['name',]
    search_fields = ['app_id', 'name', 'api_key',]
    readonly_fields = ['app_id', 'api_key',]


@admin.register(IdentityProvider)
class IdentityProviderAdmin(BaseAdmin):
    queryset_class = IdentityProvider
    list_display = ['name', 'app_id', 'api_key', 'created_at', 'updated_at',]
    ordering = ['name',]
    search_fields = ['app_id', 'name', 'api_key',]
    readonly_fields = ['app_id', 'api_key',]


@admin.register(UserIdentity)
class IdentityAdmin(BaseAdmin):
    queryset_class = UserIdentity
    list_display = ['id', 'provider', 'created_at', 'updated_at', ]
    ordering = ['-created_at',]
    readonly_fields = ['created_at', 'updated_at',]
    raw_id_fields = ['provider',]
