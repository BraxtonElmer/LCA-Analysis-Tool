from rest_framework import serializers
from .models import LCAProject, LCACalculation


class LCAProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LCAProject
        fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LCACalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LCACalculation
        fields = ['id', 'project', 'name', 'carbon_footprint', 'energy_use', 'water_use', 'created_at']
        read_only_fields = ['id', 'created_at']
