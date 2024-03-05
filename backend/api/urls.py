from django.urls import path, include
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
