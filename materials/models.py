from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class MaterialCategory(models.Model):
    """Categories for organizing materials"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Material Categories"
    
    def __str__(self):
        return self.name


class Material(models.Model):
    """Material database with properties and impact factors"""
    MATERIAL_TYPES = [
        ('metal', 'Metal'),
        ('polymer', 'Polymer'),
        ('ceramic', 'Ceramic'),
        ('composite', 'Composite'),
        ('natural', 'Natural'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    common_names = models.JSONField(default=list, blank=True, help_text="Alternative names")
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    category = models.ForeignKey(MaterialCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Basic properties
    density = models.FloatField(help_text="Density in kg/m³", validators=[MinValueValidator(0)])
    recyclable = models.BooleanField(default=True)
    recycling_efficiency = models.FloatField(
        default=0.0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Recycling efficiency percentage"
    )
    
    # Circularity properties
    durability_score = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Material durability score (0-10)"
    )
    reusability_potential = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Reusability potential percentage"
    )
    
    # Data source information
    data_source = models.CharField(max_length=100, blank=True)
    data_quality_score = models.FloatField(
        default=3.0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Data quality score (1-5)"
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    # Geographic scope
    geographic_scope = models.CharField(max_length=100, default='Global')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MaterialProperty(models.Model):
    """Properties and impact factors for materials"""
    PROPERTY_TYPES = [
        ('physical', 'Physical Property'),
        ('chemical', 'Chemical Property'),
        ('environmental', 'Environmental Impact Factor'),
        ('economic', 'Economic Property'),
        ('circularity', 'Circularity Indicator'),
    ]
    
    UNITS = [
        ('kg', 'Kilograms'),
        ('kg_co2_eq', 'kg CO2-equivalent'),
        ('kg_so2_eq', 'kg SO2-equivalent'),
        ('kg_po4_eq', 'kg PO4-equivalent'),
        ('kg_oil_eq', 'kg oil-equivalent'),
        ('kg_fe_eq', 'kg Fe-equivalent'),
        ('m3', 'Cubic meters'),
        ('m2_year', 'Square meter-years'),
        ('ctu_h', 'CTUh (Human toxicity)'),
        ('ctu_e', 'CTUe (Ecotoxicity)'),
        ('mj', 'Megajoules'),
        ('usd', 'US Dollars'),
        ('percent', 'Percentage'),
        ('dimensionless', 'Dimensionless'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='properties')
    property_name = models.CharField(max_length=100)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=20, choices=UNITS)
    
    # Uncertainty information
    uncertainty_type = models.CharField(
        max_length=20,
        choices=[
            ('none', 'No uncertainty'),
            ('range', 'Range (min-max)'),
            ('normal', 'Normal distribution'),
            ('lognormal', 'Log-normal distribution'),
        ],
        default='none'
    )
    uncertainty_value = models.FloatField(null=True, blank=True, help_text="Standard deviation or range")
    
    # Reference information
    reference = models.CharField(max_length=200, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    geographic_scope = models.CharField(max_length=100, default='Global')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['material', 'property_name', 'geographic_scope']
    
    def __str__(self):
        return f"{self.material.name} - {self.property_name}"


class RecycledMaterial(models.Model):
    """Information about recycled variants of materials"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    base_material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='recycled_variants')
    name = models.CharField(max_length=200)
    recycled_content = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of recycled content"
    )
    
    # Quality factors
    quality_factor = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Quality compared to virgin material (0-1)"
    )
    performance_factor = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Performance compared to virgin material (0-1)"
    )
    
    # Impact reduction factors
    impact_reduction_factors = models.JSONField(
        default=dict,
        help_text="Impact reduction compared to virgin material"
    )
    
    # Availability and cost
    availability_score = models.FloatField(
        default=3.0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Market availability score (1-5)"
    )
    cost_factor = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0)],
        help_text="Cost relative to virgin material"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.recycled_content}% recycled)"


class MaterialSubstitution(models.Model):
    """Potential material substitutions and their impacts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='substitution_options'
    )
    substitute_material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='substitution_targets'
    )
    
    # Substitution feasibility
    technical_feasibility = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Technical feasibility score (0-10)"
    )
    economic_feasibility = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Economic feasibility score (0-10)"
    )
    
    # Performance comparison
    performance_ratio = models.FloatField(
        default=1.0,
        help_text="Performance of substitute relative to original"
    )
    
    # Impact comparison
    environmental_benefit = models.JSONField(
        default=dict,
        help_text="Environmental impact comparison"
    )
    circularity_benefit = models.JSONField(
        default=dict,
        help_text="Circularity improvement metrics"
    )
    
    # Implementation requirements
    implementation_requirements = models.TextField(blank=True)
    barriers = models.TextField(blank=True)
    
    # Validation
    validated = models.BooleanField(default=False)
    validation_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['original_material', 'substitute_material']
    
    def __str__(self):
        return f"{self.original_material.name} → {self.substitute_material.name}"
