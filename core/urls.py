from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # O erro estava aqui. O correto é admin.site.urls
    path('admin/', admin.site.urls),
    path('', include('platform_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)