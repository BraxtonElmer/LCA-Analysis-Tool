from django.db import models
from django.contrib.auth.models import User
import uuid
import json


class AIModel(models.Model):
    """AI/ML models for LCA predictions and recommendations"""
    MODEL_TYPES = [
        ('prediction', 'Parameter Prediction'),
        ('recommendation', 'Recommendation Engine'),
        ('optimization', 'Process Optimization'),
        ('classification', 'Material Classification'),
        ('regression', 'Impact Regression'),
        ('nlp', 'Natural Language Processing'),
    ]
    
    STATUS_CHOICES = [
        ('training', 'Training'),
        ('trained', 'Trained'),
        ('deployed', 'Deployed'),
        ('deprecated', 'Deprecated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    version = models.CharField(max_length=20, default='1.0')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='training')
    
    # Model configuration
    algorithm = models.CharField(max_length=100, help_text="ML algorithm used")
    hyperparameters = models.JSONField(default=dict, help_text="Model hyperparameters")
    input_features = models.JSONField(default=list, help_text="List of input features")
    output_targets = models.JSONField(default=list, help_text="List of output targets")
    
    # Performance metrics
    accuracy_score = models.FloatField(null=True, blank=True)
    precision_score = models.FloatField(null=True, blank=True)
    recall_score = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True, help_text="Root Mean Square Error")
    mae = models.FloatField(null=True, blank=True, help_text="Mean Absolute Error")
    r2_score = models.FloatField(null=True, blank=True, help_text="R-squared score")
    
    # Training information
    training_data_size = models.PositiveIntegerField(null=True, blank=True)
    training_duration = models.FloatField(null=True, blank=True, help_text="Training time in hours")
    last_trained = models.DateTimeField(null=True, blank=True)
    
    # Model files and paths
    model_path = models.CharField(max_length=500, blank=True, help_text="Path to saved model")
    scaler_path = models.CharField(max_length=500, blank=True, help_text="Path to data scaler")
    feature_importance = models.JSONField(default=dict, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Usage statistics
    prediction_count = models.PositiveIntegerField(default=0)
    avg_prediction_time = models.FloatField(default=0.0, help_text="Average prediction time in ms")
    
    class Meta:
        unique_together = ['name', 'version']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} v{self.version} ({self.model_type})"


class TrainingDataset(models.Model):
    """Datasets used for training AI models"""
    DATASET_TYPES = [
        ('lca_data', 'LCA Historical Data'),
        ('material_properties', 'Material Properties'),
        ('process_parameters', 'Process Parameters'),
        ('environmental_impacts', 'Environmental Impacts'),
        ('circularity_metrics', 'Circularity Metrics'),
        ('expert_knowledge', 'Expert Knowledge Base'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    dataset_type = models.CharField(max_length=30, choices=DATASET_TYPES)
    
    # Dataset characteristics
    size = models.PositiveIntegerField(help_text="Number of records")
    feature_count = models.PositiveIntegerField(help_text="Number of features")
    target_count = models.PositiveIntegerField(default=1, help_text="Number of target variables")
    
    # Data quality
    completeness_score = models.FloatField(
        default=1.0, 
        help_text="Data completeness (0-1)"
    )
    quality_score = models.FloatField(
        default=3.0,
        help_text="Overall data quality (1-5)"
    )
    
    # File information
    file_path = models.CharField(max_length=500, help_text="Path to dataset file")
    file_format = models.CharField(max_length=20, default='csv')
    file_size = models.PositiveBigIntegerField(help_text="File size in bytes")
    
    # Data schema
    schema = models.JSONField(default=dict, help_text="Dataset schema definition")
    statistics = models.JSONField(default=dict, help_text="Dataset statistics")
    
    # Metadata
    source = models.CharField(max_length=200, blank=True)
    collection_date = models.DateTimeField(null=True, blank=True)
    geographic_scope = models.CharField(max_length=100, default='Global')
    temporal_scope = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.size} records)"


class Prediction(models.Model):
    """Individual predictions made by AI models"""
    PREDICTION_TYPES = [
        ('parameter_estimation', 'Parameter Estimation'),
        ('impact_prediction', 'Impact Prediction'),
        ('material_classification', 'Material Classification'),
        ('process_optimization', 'Process Optimization'),
        ('scenario_analysis', 'Scenario Analysis'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='predictions')
    prediction_type = models.CharField(max_length=30, choices=PREDICTION_TYPES)
    
    # Input data
    input_data = models.JSONField(help_text="Input features used for prediction")
    
    # Prediction results
    predictions = models.JSONField(help_text="Model predictions")
    confidence_scores = models.JSONField(default=dict, help_text="Confidence/probability scores")
    uncertainty_estimates = models.JSONField(default=dict, help_text="Uncertainty estimates")
    
    # Performance
    prediction_time = models.FloatField(help_text="Prediction time in milliseconds")
    
    # Validation (if available)
    actual_values = models.JSONField(null=True, blank=True, help_text="Actual values for validation")
    validation_metrics = models.JSONField(default=dict, help_text="Validation metrics")
    
    # Context
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project_context = models.CharField(max_length=200, blank=True)
    calculation_context = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction by {self.model.name} at {self.created_at}"


class ModelPerformanceLog(models.Model):
    """Performance monitoring for deployed models"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='performance_logs')
    
    # Performance metrics
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    f1_score = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True)
    mae = models.FloatField(null=True, blank=True)
    
    # Usage metrics
    prediction_count = models.PositiveIntegerField(default=0)
    avg_prediction_time = models.FloatField(default=0.0)
    error_count = models.PositiveIntegerField(default=0)
    
    # Data drift detection
    data_drift_score = models.FloatField(null=True, blank=True)
    model_drift_score = models.FloatField(null=True, blank=True)
    
    # Time period
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    
    # Additional metrics
    custom_metrics = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Performance log for {self.model.name} ({self.period_start.date()})"


class NLQueryLog(models.Model):
    """Log of natural language queries and responses"""
    QUERY_TYPES = [
        ('what_if', 'What-if Analysis'),
        ('comparison', 'Scenario Comparison'),
        ('recommendation', 'Recommendation Request'),
        ('explanation', 'Result Explanation'),
        ('data_query', 'Data Query'),
        ('general', 'General Question'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query_text = models.TextField(help_text="Original natural language query")
    query_type = models.CharField(max_length=20, choices=QUERY_TYPES)
    
    # Processing
    processed_query = models.JSONField(help_text="Processed/structured query")
    intent_classification = models.CharField(max_length=100, blank=True)
    entities_extracted = models.JSONField(default=list)
    
    # Response
    response_text = models.TextField(help_text="Generated response")
    response_data = models.JSONField(default=dict, help_text="Structured response data")
    confidence_score = models.FloatField(default=0.0)
    
    # Performance
    processing_time = models.FloatField(help_text="Total processing time in seconds")
    
    # User feedback
    user_rating = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="User rating (1-5)"
    )
    user_feedback = models.TextField(blank=True)
    
    # Context
    project_context = models.CharField(max_length=200, blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query: {self.query_text[:50]}..."
