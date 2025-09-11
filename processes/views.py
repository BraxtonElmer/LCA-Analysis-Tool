from rest_framework import viewsets
from .models import Process, ProcessParameter
from rest_framework.permissions import IsAuthenticated


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # Import here to avoid circular imports
        from .serializers import ProcessSerializer
        return ProcessSerializer


class ProcessParameterViewSet(viewsets.ModelViewSet):
    queryset = ProcessParameter.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import ProcessParameterSerializer
        return ProcessParameterSerializer
