from rest_framework import viewsets
from .models import CircularityIndicator, CircularityAnalysis
from rest_framework.permissions import IsAuthenticated


class CircularityIndicatorViewSet(viewsets.ModelViewSet):
    queryset = CircularityIndicator.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import CircularityIndicatorSerializer
        return CircularityIndicatorSerializer


class CircularityAnalysisViewSet(viewsets.ModelViewSet):
    queryset = CircularityAnalysis.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import CircularityAnalysisSerializer
        return CircularityAnalysisSerializer
