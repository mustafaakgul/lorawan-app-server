from django import forms
from .models import Gateways

class GatewayForm(forms.ModelForm):
    class Meta:
        model = Gateways
        fields = ["gatewayName", "gatewayDescription", "gatewayEui"]