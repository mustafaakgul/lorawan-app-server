from django.contrib import admin
from .models import Endnode


@admin.register(Endnode)
class EndnodeAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "status"]
    list_display_links = ["name"]
    search_fields = ["name"]
    list_filter = ["created_date"]
    class Meta:
        model = Endnode
