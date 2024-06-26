"""  from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from endnodes.models import EndDevice
from .serializers import EndDeviceSerializer


class EndDeviceListView(ListAPIView):
    queryset = EndDevice.objects.all()
    serializer_class = EndDeviceSerializer
    permission_classes = (permissions.AllowAny, )


class EndDeviceDetailView(RetrieveAPIView):
    queryset = EndDevice.objects.all()
    serializer_class = EndDeviceSerializer
    permission_classes = (permissions.AllowAny, )
"""
from rest_framework import viewsets
from enddevices.models import EndDevice
from .serializers import EndDeviceSerializer

class EndDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = EndDeviceSerializer
    queryset = EndDevice.objects.all()