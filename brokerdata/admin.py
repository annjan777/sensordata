from django.contrib import admin
from .models import SensorData

class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('topic', 'timestamp', 'data')
    list_filter = ('topic', 'timestamp')
    search_fields = ('topic', 'data')

admin.site.register(SensorData, SensorDataAdmin)
