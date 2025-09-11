from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LCAProject, LCACalculation
from .serializers import LCAProjectSerializer, LCACalculationSerializer


class LCAProjectViewSet(viewsets.ModelViewSet):
    """Simplified ViewSet for LCA Projects"""
    serializer_class = LCAProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LCAProject.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LCACalculationViewSet(viewsets.ModelViewSet):
    """Simplified ViewSet for LCA Calculations"""
    serializer_class = LCACalculationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LCACalculation.objects.filter(project__owner=self.request.user)
