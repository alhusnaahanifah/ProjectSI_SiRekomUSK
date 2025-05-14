from django.urls import path
from . import views

urlpatterns = [
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('daftar-pengguna/', views.daftar_pengguna, name='daftar_pengguna'),
    path('daftar-prodi/', views.daftar_prodi, name='daftar_prodi'),
    # urls.py
    path('hapus_pengguna/<str:user_id>/', views.hapus_pengguna, name='hapus_pengguna'),
    path('hapus_prodi/<str:prodi_id>/', views.hapus_prodi, name='hapus_prodi'),
    path('edit/<str:prodi_id>/', views.edit_prodi, name='edit_prodi'),
]