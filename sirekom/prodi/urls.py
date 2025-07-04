from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,  name='dashboard_siswa'),
    path('tambah-prodi/', views.tambah_prodi, name='tambah_prodi'),
    path('prodi/', views.daftar_prodi, name='daftar_prodi'),
    path('tambah-fakultas/', views.tambah_fakultas, name='tambah_fakultas'),
    path('daftar-fakultas/', views.daftar_fakultas, name='daftar_fakultas'),
    path('fakultas/<str:fakultas_id>/', views.detail_prodi, name='detail_prodi'),
    path('fakultas/edit/<str:fakultas_id>/', views.edit_fakultas, name='edit_fakultas'),
    path('fakultas/hapus/<str:fakultas_id>/', views.hapus_fakultas, name='hapus_fakultas'),
]
