from django.contrib import admin
from .models import WebUser


@admin.register(WebUser)
class WebUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'is_staff')
    list_display_links = ('username',)
    search_fields = ('email', 'username')
    list_filter = ('email', 'username')
