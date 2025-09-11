from rest_framework import viewsets
from .models import AIModel, Prediction
from rest_framework.permissions import IsAuthenticated


class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import AIModelSerializer
        return AIModelSerializer


class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import PredictionSerializer
        return PredictionSerializer
