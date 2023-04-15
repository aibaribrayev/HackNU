from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, ZakupkiViewSet, SalesViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'zakupki', ZakupkiViewSet)
router.register(r'sales', SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
