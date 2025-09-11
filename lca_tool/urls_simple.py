# Simplified URLs for quick start
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def api_status(request):
    return JsonResponse({
        'status': 'running',
        'message': 'AI-Driven LCA Analysis Tool API is running!',
        'version': '1.0.0'
    })

def dashboard_stats(request):
    return JsonResponse({
        'total_projects': 0,
        'completed_assessments': 0,
        'co2_saved': 0,
        'avg_circularity_score': 0,
        'message': 'Demo data - connect to database for real statistics'
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/status/', api_status, name='api_status'),
    path('api/dashboard/', dashboard_stats, name='dashboard_stats'),
]
