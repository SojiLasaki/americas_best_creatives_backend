from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Local fallback: allow runserver to serve collected static/media when DEBUG is False.
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
