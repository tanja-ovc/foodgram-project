from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('api.urls')),
    path('api/', include('djoser.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
