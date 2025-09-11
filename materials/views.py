from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Material, MaterialProperty, RecycledMaterial, MaterialSubstitution
from .serializers import (
    MaterialSerializer, MaterialPropertySerializer, 
    RecycledMaterialSerializer, MaterialSubstitutionSerializer
)
from .services import MaterialDatabaseService, MaterialRecommendationService


class MaterialViewSet(viewsets.ModelViewSet):
    """ViewSet for materials database"""
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Material.objects.all()
        
        # Filter by search query
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(common_names__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Filter by material type
        material_type = self.request.query_params.get('type')
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        
        # Filter by recyclable
        recyclable = self.request.query_params.get('recyclable')
        if recyclable is not None:
            queryset = queryset.filter(recyclable=recyclable.lower() == 'true')
        
        return queryset.order_by('name')
    
    @action(detail=True, methods=['get'])
    def impact_factors(self, request, pk=None):
        """Get environmental impact factors for a material"""
        material = self.get_object()
        
        impact_factors = {}
        for prop in material.properties.filter(property_type='environmental'):
            impact_factors[prop.property_name] = {
                'value': prop.value,
                'unit': prop.unit,
                'uncertainty': prop.uncertainty_value,
                'reference': prop.reference
            }
        
        return Response({
            'material': material.name,
            'impact_factors': impact_factors
        })
    
    @action(detail=True, methods=['get'])
    def alternatives(self, request, pk=None):
        """Get alternative materials and substitutions"""
        material = self.get_object()
        
        # Get direct substitutions
        substitutions = MaterialSubstitution.objects.filter(
            original_material=material
        ).select_related('substitute_material')
        
        # Get recycled variants
        recycled_variants = material.recycled_variants.all()
        
        # Use AI service to find similar materials
        service = MaterialRecommendationService()
        similar_materials = service.find_similar_materials(material)
        
        alternatives_data = {
            'substitutions': MaterialSubstitutionSerializer(substitutions, many=True).data,
            'recycled_variants': RecycledMaterialSerializer(recycled_variants, many=True).data,
            'similar_materials': similar_materials,
        }
        
        return Response(alternatives_data)
    
    @action(detail=False, methods=['post'])
    def bulk_import(self, request):
        """Bulk import materials from uploaded file"""
        service = MaterialDatabaseService()
        
        try:
            file_obj = request.FILES.get('file')
            if not file_obj:
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            results = service.import_materials_from_file(file_obj)
            
            return Response({
                'message': f"Imported {results['imported']} materials",
                'imported': results['imported'],
                'skipped': results['skipped'],
                'errors': results['errors']
            })
            
        except Exception as e:
            return Response(
                {'error': 'Import failed', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MaterialPropertyViewSet(viewsets.ModelViewSet):
    """ViewSet for material properties"""
    serializer_class = MaterialPropertySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = MaterialProperty.objects.select_related('material')
        
        # Filter by material
        material_id = self.request.query_params.get('material')
        if material_id:
            queryset = queryset.filter(material_id=material_id)
        
        # Filter by property type
        prop_type = self.request.query_params.get('type')
        if prop_type:
            queryset = queryset.filter(property_type=prop_type)
        
        return queryset.order_by('material__name', 'property_name')


class RecycledMaterialViewSet(viewsets.ModelViewSet):
    """ViewSet for recycled materials"""
    serializer_class = RecycledMaterialSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RecycledMaterial.objects.select_related('base_material').order_by('name')


class MaterialSubstitutionViewSet(viewsets.ModelViewSet):
    """ViewSet for material substitutions"""
    serializer_class = MaterialSubstitutionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MaterialSubstitution.objects.select_related(
            'original_material', 'substitute_material'
        ).order_by('original_material__name')
    
    @action(detail=False, methods=['post'])
    def analyze_substitution(self, request):
        """Analyze potential substitution between two materials"""
        original_id = request.data.get('original_material_id')
        substitute_id = request.data.get('substitute_material_id')
        
        if not original_id or not substitute_id:
            return Response(
                {'error': 'Both original_material_id and substitute_material_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            service = MaterialRecommendationService()
            analysis = service.analyze_substitution(original_id, substitute_id)
            
            return Response({
                'analysis': analysis,
                'recommendation': analysis.get('recommendation', 'neutral')
            })
            
        except Exception as e:
            return Response(
                {'error': 'Analysis failed', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
