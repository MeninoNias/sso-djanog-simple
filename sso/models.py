from django.db import models

from authentication.models import BaseModel, IdentityProvider


# Create your models here.

class AccessIdentity(BaseModel):
    class Meta:
        verbose_name = 'access identity'
        verbose_name_plural = 'access identities'

    provider = models.ForeignKey(IdentityProvider, on_delete=models.CASCADE)

    data = models.TextField()
    status_code = models.IntegerField()

    def __str__(self):
        return str(self.pk)
