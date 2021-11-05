from rest_framework import serializers
from Enddevice.models import EndDevice

class EndDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndDevice
        fields = ('id', 'name', 'description', "activation_method", "last_value", "rssi", "snr", "status")