import uuid
import requests

from django.db import models
from django.db.models import QuerySet, ProtectedError


class BaseModelQuerySet(QuerySet):

    def delete(self):
        [x.delete() for x in self]

    def hard_delete(self):
        [x.hard_delete() for x in self]

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class BaseModelManager(models.Manager):
    use_for_related_fields = True

    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(BaseModelManager, self).__init__(*args, **kwargs)

    def all_objects(self):
        return BaseModelQuerySet(self.model)

    def get_queryset(self):
        if self.active_only:
            return BaseModelQuerySet(self.model).filter(is_active=True)
        return BaseModelQuerySet(self.model)

    def hard_delete(self):
        self.get_queryset().hard_delete()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = BaseModelManager()
    all_objects = BaseModelManager(active_only=False)

    def _on_delete(self):
        for relation in self._meta._relation_tree:
            on_delete = getattr(relation.remote_field, 'on_delete')

            if on_delete in [None, models.DO_NOTHING]:
                continue

            filter = {relation.name: self}
            related_queryset = relation.model.objects.filter(**filter)

            if on_delete == models.CASCADE:
                relation.model.objects.filter(**filter).delete()
            elif on_delete == models.SET_NULL:
                for r in related_queryset.all():
                    related_queryset.update(**{relation.name: None})
            elif on_delete == models.PROTECT:
                if related_queryset.count() > 0:
                    raise ProtectedError('Cannot remove this instances', related_queryset.all())
            else:
                raise NotImplementedError()

    def delete(self):
        self.is_active = False
        self.save()
        self._on_delete()

    def hard_delete(self):
        super(BaseModel, self).delete()

    class Meta:
        abstract = True


class Client(BaseModel):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=40, unique=True, editable=False, default=uuid.uuid4)

    @property
    def app_id(self):
        return self.pk

    def __str__(self):
        return self.name


class IdentityProvider(BaseModel):
    class Meta:
        verbose_name = 'Provedor de identidade'
        verbose_name_plural = 'Provedores de identidade'

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='identity_providers')

    name = models.CharField(max_length=255)
    host = models.URLField()
    custom_url = models.CharField(max_length=255, blank=True, null=True,
                                  help_text='Custom URL o padrão é (api/singin)')
    api_key = models.CharField(max_length=40, unique=True, editable=False, default=uuid.uuid4)

    @property
    def app_id(self):
        return self.pk

    def connection(self, username, password):
        data = {'email': username, 'password': password}

        path = self.custom_url if self.custom_url else 'api/singin'
        url = f'{self.host}/{path}'

        return requests.post(
            url,
            json=data,
            auth=(self.app_id, self.api_key),
            timeout=5
        )

    def __str__(self):
        return f'{self.client.name} - {self.name}'


class UserIdentity(BaseModel):
    class Meta:
        verbose_name = 'Identidade do usuario'
        verbose_name_plural = 'Identidades dos usuarios'

    provider = models.ForeignKey(IdentityProvider, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    external_id = models.CharField(max_length=255, default='id')
    name = models.CharField(max_length=255, default='unknown')
    username = models.CharField(max_length=255, default='unknown')
    email = models.EmailField(default='unknown')

    def __str__(self):
        return str(self.pk)
