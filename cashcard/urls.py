from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CashCardViewSet

router = DefaultRouter()
router.register(r'', CashCardViewSet, basename='cashcard')

urlpatterns = [
    path('', include(router.urls)),
]
