from django.contrib import admin
from .models import UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'method', 'path',  'response_status', 'response_message')
    list_filter = ('method',  'response_status', 'timestamp')
    search_fields = ('user__username', 'path', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'path', 'method', 'request_data', 'response_status',
                      'ip_address', 'user_agent', 'response_message', 'custom_fields')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
