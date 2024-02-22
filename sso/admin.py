from django.contrib import admin

from authentication.admin import BaseAdmin
from sso.models import AccessIdentity


# Register your models here.
@admin.register(AccessIdentity)
class SharedIdentityAdmin(BaseAdmin):
    queryset_class = AccessIdentity
    raw_id_fields = ['provider', ]
    list_display = ('id', 'created_at', 'updated_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at',)