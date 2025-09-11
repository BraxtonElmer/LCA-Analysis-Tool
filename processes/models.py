from django.db import models
import uuid


class ProcessCategory(models.Model):
    """Categories for organizing processes"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Process Categories"
    
    def __str__(self):
        return self.name


class Process(models.Model):
    """Industrial processes with environmental impact factors"""
    PROCESS_TYPES = [
        ('extraction', 'Raw Material Extraction'),
        ('processing', 'Material Processing'),
        ('manufacturing', 'Manufacturing'),
        ('transport', 'Transportation'),
        ('energy', 'Energy Production'),
        ('waste_treatment', 'Waste Treatment'),
        ('recycling', 'Recycling'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    process_type = models.CharField(max_length=20, choices=PROCESS_TYPES)
    category = models.ForeignKey(ProcessCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Process characteristics
    input_materials = models.JSONField(default=list, help_text="Input materials and quantities")
    output_materials = models.JSONField(default=list, help_text="Output materials and quantities")
    energy_requirements = models.JSONField(default=dict, help_text="Energy requirements by type")
    
    # Environmental impact factors (per functional unit)
    impact_factors = models.JSONField(default=dict, help_text="Environmental impact factors")
    
    # Technical parameters
    efficiency = models.FloatField(default=1.0, help_text="Process efficiency (0-1)")
    capacity = models.FloatField(null=True, blank=True, help_text="Process capacity")
    capacity_unit = models.CharField(max_length=50, blank=True)
    
    # Geographic and temporal scope
    geographic_scope = models.CharField(max_length=100, default='Global')
    temporal_scope = models.CharField(max_length=100, blank=True)
    
    # Data quality
    data_source = models.CharField(max_length=100, blank=True)
    data_quality_score = models.FloatField(default=3.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProcessParameter(models.Model):
    """Parameters and variables for processes"""
    PARAMETER_TYPES = [
        ('input', 'Input Parameter'),
        ('output', 'Output Parameter'),
        ('efficiency', 'Efficiency Parameter'),
        ('environmental', 'Environmental Parameter'),
        ('economic', 'Economic Parameter'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=100)
    parameter_type = models.CharField(max_length=20, choices=PARAMETER_TYPES)
    
    # Parameter properties
    default_value = models.FloatField()
    unit = models.CharField(max_length=50)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    
    # Uncertainty
    uncertainty_type = models.CharField(max_length=20, default='none')
    uncertainty_value = models.FloatField(null=True, blank=True)
    
    # Metadata
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=200, blank=True)
    
    class Meta:
        unique_together = ['process', 'name']
    
    def __str__(self):
        return f"{self.process.name} - {self.name}"
