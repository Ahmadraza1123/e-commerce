from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    LogoutViewSet,
    UserProfileView,
    RequestPasswordReset,
    PasswordResetConfirmView,LoginView
)

router = DefaultRouter()
router.register(r'register', UserViewSet, basename='users')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('', include(router.urls)),

    # Auth routes
    path('login/', LoginView.as_view(), name='api-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password-reset/', RequestPasswordReset.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
