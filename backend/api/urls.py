from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

urlpatterns = [
    path('', include('api.users.urls')),
    path('', include('api.recipes.urls')),
]
