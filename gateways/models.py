from django.db import models


class Gateways(models.Model):
    gatewayTypes = (
        ("0", "Indoor"),
        ("1", "Outdoor")
    )
    gatewayName = models.CharField(max_length=50, verbose_name="Gateway Name")
    gatewayEui = models.CharField(max_length=50, verbose_name="Gateway EUI")
    gatewayDescription = models.CharField(max_length=100, verbose_name="Gateway Description")
    typeofGateway = models.CharField(max_length=50, choices=gatewayTypes, default="0",
                                     verbose_name="Type of Gateway")
    gatewayCreatedDate = models.DateTimeField(auto_created=True, verbose_name="Created Date")
    gatewayLatitude = models.FloatField(max_length=50, verbose_name="Gateway Latitude")
    gatewayLongitude = models.FloatField(max_length=50, verbose_name="Gateway Longitude")
    author = models.ForeignKey("auth.User", on_delete=models.PROTECT, null=True)
    gatewayStatus = models.CharField(max_length=50, verbose_name="Gateway Status", null=True)
    gatewayLastSeen = models.TextField(null=True)

    def __str__(self):
        return self.gatewayName, self.gatewayDescription


class GatewayInternalInformations(models.Model):
    gatewayEui = models.CharField(max_length=50, verbose_name="Gateway EUI", null=True)
    typeofGatewayInternal = models.CharField(max_length=50,default="Indoor", verbose_name="Type of Gateway", null=True)
    author = models.ForeignKey("auth.User", on_delete=models.PROTECT, null=True)