from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static




admin.site.site_header = "QR Generator Admin"
admin.site.site_title = "QR Generator Portal"
admin.site.index_title = "Welcome to QR Generator Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('qrapp.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)