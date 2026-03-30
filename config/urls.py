from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.stations.urls')),
    path('api/', include('apps.catalog.urls')),
    path('api/', include('apps.quotes.urls')),
    path('api/', include('apps.designs.urls')),
    path('api/', include('apps.payments.urls')),
    path('api/', include('apps.chat.urls')),
    path('api/', include('apps.notifications.urls')),
    path('api/', include('apps.disputes.urls')),
    path('api/', include('apps.support.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
