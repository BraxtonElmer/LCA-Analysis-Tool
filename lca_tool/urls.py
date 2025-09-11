from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

# Import simplified API viewsets
from lca_core.views import LCAProjectViewSet, LCACalculationViewSet
from lca_core.home_views import home, api_status

# Create API router
router = DefaultRouter()
router.register(r'projects', LCAProjectViewSet, basename='lcaproject')
router.register(r'calculations', LCACalculationViewSet, basename='lcacalculation')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/status/', api_status, name='api_status'),
    path('api/auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
