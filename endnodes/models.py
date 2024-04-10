from django.db import models


class Endnode(models.Model):

    author = models.ForeignKey("auth.User", on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    activation_method = models.CharField(max_length=50, default = "ABP", null=True, blank = True)
    device_type = models.CharField(max_length=50, null=True)
    last_value = models.CharField(max_length=50, null=True)
    rssi = models.CharField(max_length=50, null=True)
    snr = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50)
    dev_eui = models.CharField(max_length=50, verbose_name="Device EUI", null=True)
    app_eui = models.CharField(max_length=50, verbose_name="Application EUI", null=True)
    dev_add = models.CharField(max_length=50, verbose_name="Device Address", null=True)
    net_sess_key = models.CharField(max_length=50, verbose_name="Network Session Key", null=True)
    app_sess_key = models.CharField(max_length=50, verbose_name="Application Session Key", null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
