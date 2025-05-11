from django.urls import path
from . import views

urlpatterns = [
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('daftar-pengguna/', views.daftar_pengguna, name='daftar_pengguna'),
]