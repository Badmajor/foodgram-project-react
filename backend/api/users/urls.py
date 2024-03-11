from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SubscriptionViewSet, UserViewSetWithActions

router = DefaultRouter()
router.register(r'users/subscriptions', SubscriptionViewSet, basename='subscriptions')
router.register('users', UserViewSetWithActions, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
