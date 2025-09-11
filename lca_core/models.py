from django.db import models
from django.contrib.auth.models import User


class LCAProject(models.Model):
    """Simplified LCA Project model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LCACalculation(models.Model):
    """Basic LCA Calculation model"""
    project = models.ForeignKey(LCAProject, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    carbon_footprint = models.FloatField(default=0.0, help_text="kg CO2 eq")
    energy_use = models.FloatField(default=0.0, help_text="MJ")
    water_use = models.FloatField(default=0.0, help_text="liters")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"
