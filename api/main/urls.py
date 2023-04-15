
from django.urls import path, include
from rest_framework import routers
from .views import SalesViewSet

router = routers.DefaultRouter()
router.register(r'sales', SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
