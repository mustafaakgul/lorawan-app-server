"""from django.urls import path

from .views import (
    EndDeviceListView,
    EndDeviceDetailView,
)

urlpatterns = [
    path('', EndDeviceListView.as_view()),
    path('<pk>', EndDeviceDetailView.as_view()),
]"""

from enddevices.api.views import EndDeviceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', EndDeviceViewSet)
urlpatterns = router.urls