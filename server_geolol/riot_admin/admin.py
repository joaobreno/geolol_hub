from django.contrib import admin
from .models import *

class AdminSettings(admin.ModelAdmin):
    list_display = ['riot_api_key']

admin.site.register(AdminSet, AdminSettings)