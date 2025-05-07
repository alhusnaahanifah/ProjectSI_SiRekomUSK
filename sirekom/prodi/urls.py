from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard),
    path('tambah-prodi/', views.tambah_prodi, name='tambah_prodi'),
    path('prodi/', views.daftar_prodi, name='daftar_prodi'),
    path('tambah-fakultas/', views.tambah_fakultas, name='tambah_fakultas'),
    path('daftar-fakultas/', views.daftar_fakultas, name='daftar_fakultas'),
]