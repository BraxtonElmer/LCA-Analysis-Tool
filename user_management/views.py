from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return []

    def get_serializer_class(self):
        from rest_framework import serializers
        class DummySerializer(serializers.Serializer):
            pass
        return DummySerializer
