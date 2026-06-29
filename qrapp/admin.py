from django.contrib import admin
from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'url', 'short_code', 'is_active', 'scans', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'url', 'short_code')
    readonly_fields = ('qr_image', 'created_at', 'scans', 'short_code')
    ordering = ('-created_at',)
    list_per_page = 20
