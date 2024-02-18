from django.urls import path

from authentication.api.v1.views import ClientAPIView

urlpatterns = [
    path('client', ClientAPIView.as_view(), name='client-reatrive'),
]