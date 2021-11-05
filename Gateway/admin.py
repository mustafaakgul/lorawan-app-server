from django.contrib import admin
from . models import Gateways

@admin.register(Gateways)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ["gatewayName", "gatewayDescription", "gatewayStatus"]
    list_display_links = ["gatewayName"]
    search_fields = ["gatewayName"]
    list_filter = ["gatewayCreatedDate"]
    class Meta:
        model = Gateways

