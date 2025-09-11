from django.contrib import admin
from .models import LCAProject, LCACalculation


@admin.register(LCAProject)
class LCAProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LCACalculation)
class LCACalculationAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'carbon_footprint', 'energy_use', 'water_use', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'project__name']
    readonly_fields = ['created_at']
