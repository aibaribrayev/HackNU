
from django.urls import path, include
from rest_framework import routers
from .views import SalesViewSet, SupplyViewSet

router = routers.DefaultRouter()
router.register(r'supplies', SupplyViewSet)
router.register(r'sales', SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
