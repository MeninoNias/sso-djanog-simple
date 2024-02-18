from django.urls import path

from sso.api.v1.views import LoginAPIView

urlpatterns = [
    path('v1/login/', LoginAPIView.as_view(), name='client-reatrive'),
]
