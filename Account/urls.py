from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginViewSet, LogoutViewSet

router = DefaultRouter()
router.register(r'register', UserViewSet, basename='user')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls)),
]
