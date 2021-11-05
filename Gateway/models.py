from django.db import models


class Gateways(models.Model):
    gatewayName = models.CharField(max_length=50, verbose_name="Gateway Name")
    gatewayEui = models.CharField(max_length=50, verbose_name="Gateway EUI", null=True)
    gatewayDescription = models.CharField(max_length=100, verbose_name="Gateway Description")
    typeofGateway = models.CharField(max_length=50, default="Indoor", verbose_name="Type of Gateway", null=True)
    gatewayCreatedDate = models.TextField(null=True)
    gatewayLatitude = models.FloatField(max_length=50, verbose_name="Gateway Latitude", null=True)
    gatewayLongitude = models.FloatField(max_length=50, verbose_name="Gateway Longitude", null=True)
    author = models.ForeignKey("auth.User", on_delete=models.PROTECT, null=True)
    gatewayStatus = models.CharField(max_length=50, verbose_name="Gateway Status", null=True)
    gatewayLastSeen = models.TextField(null=True)

    def __str__(self):
        return self.gatewayName

"""
class GatewayInternalInformations(models.Model):
    gatewayEui = models.CharField(max_length=50, verbose_name="Gateway EUI", null=True)
    typeofGatewayInternal = models.CharField(max_length=50, default="Indoor", verbose_name="Type of Gateway", null=True)
    author = models.ForeignKey("auth.User", on_delete=models.PROTECT, null=True)


"""

