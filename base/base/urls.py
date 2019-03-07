from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

swaggerView = get_swagger_view(title='Hello Swagger API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    # path('swagger/', swaggerView),

    path('', include('apis.urls')),
    path('auth/', include('auths.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
