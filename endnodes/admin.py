from django.contrib import admin

from .models import EndDevice


admin.site.register(EndDevice)
#@admin.register(EndDevice)
"""class EndnodeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "status"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["created_date"]
    class Meta:
        model = EndDevice"""
