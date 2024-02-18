from django.urls import path, include

urlpatterns = [
    path('', include('sso.api.urls')),
]
