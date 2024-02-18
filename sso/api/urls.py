from django.urls import path, include

urlpatterns = [
    path('api/', include('sso.api.v1.urls')),
]