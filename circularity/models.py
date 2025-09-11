from django.db import models
from django.contrib.auth.models import User
import uuid


class CircularityIndicator(models.Model):
    """Circularity indicators and metrics"""
    INDICATOR_TYPES = [
        ('material_flow', 'Material Flow'),
        ('recycling', 'Recycling'),
        ('reuse', 'Reuse'),
        ('lifetime_extension', 'Lifetime Extension'),
        ('resource_efficiency', 'Resource Efficiency'),
        ('waste_reduction', 'Waste Reduction'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    indicator_type = models.CharField(max_length=20, choices=INDICATOR_TYPES)
    
    # Calculation method
    calculation_method = models.TextField(help_text="Description of calculation method")
    formula = models.TextField(blank=True, help_text="Mathematical formula")
    
    # Units and ranges
    unit = models.CharField(max_length=50)
    min_value = models.FloatField(default=0)
    max_value = models.FloatField(default=100)
    target_value = models.FloatField(null=True, blank=True, help_text="Target or benchmark value")
    
    # Weighting for overall circularity score
    weight = models.FloatField(default=1.0, help_text="Weight for overall circularity calculation")
    
    # Data requirements
    required_data = models.JSONField(default=list, help_text="List of required data inputs")
    
    # Metadata
    reference_standard = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CircularityAnalysis(models.Model):
    """Circularity analysis for LCA calculations"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    calculation = models.OneToOneField(
        'lca_core.LCACalculation',
        on_delete=models.CASCADE,
        related_name='circularity_analysis'
    )
    
    # Overall circularity metrics
    overall_circularity_score = models.FloatField(default=0.0)
    material_circularity_score = models.FloatField(default=0.0)
    component_circularity_score = models.FloatField(default=0.0)
    
    # Specific indicators
    recycled_content_rate = models.FloatField(default=0.0, help_text="Percentage of recycled content")
    recyclability_rate = models.FloatField(default=0.0, help_text="Percentage of recyclable materials")
    reuse_potential = models.FloatField(default=0.0, help_text="Reuse potential score")
    lifetime_extension_factor = models.FloatField(default=1.0)
    material_efficiency = models.FloatField(default=0.0)
    
    # Material flow indicators
    virgin_material_input = models.FloatField(default=0.0)
    recycled_material_input = models.FloatField(default=0.0)
    material_losses = models.FloatField(default=0.0)
    waste_output = models.FloatField(default=0.0)
    recovered_materials = models.FloatField(default=0.0)
    
    # Detailed analysis results
    indicator_results = models.JSONField(default=dict, help_text="Results for each circularity indicator")
    improvement_opportunities = models.JSONField(default=list)
    circularity_strategies = models.JSONField(default=list)
    
    # Benchmarking
    benchmark_comparison = models.JSONField(default=dict, blank=True)
    industry_percentile = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Circularity Analysis - {self.calculation.name}"


class CircularityBenchmark(models.Model):
    """Benchmarks for circularity indicators by industry/sector"""
    SECTORS = [
        ('metallurgy', 'Metallurgy'),
        ('mining', 'Mining'),
        ('construction', 'Construction'),
        ('electronics', 'Electronics'),
        ('automotive', 'Automotive'),
        ('packaging', 'Packaging'),
        ('textiles', 'Textiles'),
        ('general', 'General Manufacturing'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    indicator = models.ForeignKey(CircularityIndicator, on_delete=models.CASCADE)
    sector = models.CharField(max_length=20, choices=SECTORS)
    
    # Benchmark values
    best_practice_value = models.FloatField(help_text="Best practice benchmark")
    industry_average = models.FloatField(help_text="Industry average")
    minimum_acceptable = models.FloatField(help_text="Minimum acceptable level")
    
    # Percentile distributions
    percentile_25 = models.FloatField(null=True, blank=True)
    percentile_50 = models.FloatField(null=True, blank=True)
    percentile_75 = models.FloatField(null=True, blank=True)
    percentile_90 = models.FloatField(null=True, blank=True)
    
    # Data source
    data_source = models.CharField(max_length=200)
    sample_size = models.PositiveIntegerField(null=True, blank=True)
    year = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['indicator', 'sector', 'year']
    
    def __str__(self):
        return f"{self.indicator.name} - {self.sector} ({self.year})"


class CircularityImprovement(models.Model):
    """Circularity improvement suggestions and strategies"""
    IMPROVEMENT_TYPES = [
        ('material_substitution', 'Material Substitution'),
        ('design_change', 'Design Change'),
        ('process_optimization', 'Process Optimization'),
        ('supply_chain', 'Supply Chain'),
        ('end_of_life', 'End-of-Life Management'),
        ('business_model', 'Business Model'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    analysis = models.ForeignKey(
        CircularityAnalysis,
        on_delete=models.CASCADE,
        related_name='improvements'
    )
    
    # Improvement details
    title = models.CharField(max_length=200)
    description = models.TextField()
    improvement_type = models.CharField(max_length=25, choices=IMPROVEMENT_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    
    # Impact assessment
    potential_impact_score = models.FloatField(help_text="Potential improvement in circularity score")
    implementation_effort = models.FloatField(
        default=5.0,
        help_text="Implementation effort score (1-10)"
    )
    cost_estimate = models.FloatField(null=True, blank=True, help_text="Implementation cost estimate")
    
    # Implementation details
    implementation_steps = models.JSONField(default=list)
    required_resources = models.JSONField(default=list)
    timeline_estimate = models.CharField(max_length=100, blank=True)
    
    # Barriers and risks
    implementation_barriers = models.JSONField(default=list)
    risks = models.JSONField(default=list)
    success_factors = models.JSONField(default=list)
    
    # Validation
    is_validated = models.BooleanField(default=False)
    validation_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-priority', '-potential_impact_score']
    
    def __str__(self):
        return f"{self.title} ({self.priority})"


class CircularityStrategy(models.Model):
    """Pre-defined circularity strategies and best practices"""
    STRATEGY_CATEGORIES = [
        ('design', 'Design for Circularity'),
        ('materials', 'Material Selection'),
        ('manufacturing', 'Manufacturing'),
        ('distribution', 'Distribution'),
        ('use_phase', 'Use Phase'),
        ('end_of_life', 'End of Life'),
        ('business_model', 'Business Model'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=STRATEGY_CATEGORIES)
    
    # Strategy details
    objectives = models.JSONField(default=list, help_text="Strategy objectives")
    key_actions = models.JSONField(default=list, help_text="Key actions to implement")
    success_metrics = models.JSONField(default=list, help_text="Metrics to measure success")
    
    # Applicability
    applicable_sectors = models.JSONField(default=list)
    applicable_materials = models.JSONField(default=list)
    applicable_processes = models.JSONField(default=list)
    
    # Expected benefits
    environmental_benefits = models.JSONField(default=list)
    economic_benefits = models.JSONField(default=list)
    social_benefits = models.JSONField(default=list)
    
    # Implementation guidance
    implementation_guide = models.TextField(blank=True)
    case_studies = models.JSONField(default=list)
    references = models.JSONField(default=list)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
