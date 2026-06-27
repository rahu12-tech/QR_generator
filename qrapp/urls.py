from django.urls import path
from . import views

urlpatterns = [
   path('dashboard/', views.dashboard, name='dashboard'),
    path('my-qrs/', views.my_qrs, name='my_qrs'),
    path('active-qrs/', views.active_qrs, name='active_qrs'),
    path('paused-qrs/', views.paused_qrs, name='paused_qrs'),
    path('delete-qr/<int:id>/', views.delete_qr, name='delete_qr'),
    path('toggle-qr/<int:id>/', views.toggle_qr, name='toggle_qr'),
    path('edit-qr/<int:id>/', views.edit_qr, name='edit_qr'),
    path('s/<str:short_code>/', views.short_redirect, name='short_redirect'),
    path('scan/<int:id>/',views.scan_qr, name='scan_qr')
   ]