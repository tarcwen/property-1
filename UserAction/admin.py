from django.contrib import admin
from .models import UserAction

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ['user__username', 'action']
