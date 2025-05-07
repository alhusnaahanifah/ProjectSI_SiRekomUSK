# views.py
from django.shortcuts import render, redirect
from .forms import ProdiForm
from .models import Prodi
from django.http import JsonResponse
from .forms import FakultasForm
from .models import Fakultas
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
def dashboard(request):
  semua_fakultas = Fakultas.objects.all()
  return render(request, 'prodi/dashboard.html', {'fakultas_list': semua_fakultas})

def tambah_prodi(request):
    if request.method == 'POST':
        form = ProdiForm(request.POST, request.FILES)  # Pastikan request.FILES ditangani di form
        if form.is_valid():
            # Mendapatkan file yang di-upload
            uploaded_file = request.FILES['gambar']
            
            # Menyimpan file gambar ke folder media
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)
            mata_kuliah_list = form.cleaned_data['mata_kuliah_unggulan'].split(',')
            prospek_kerja_list = form.cleaned_data['prospek_kerja'].split(',')


            # Membuat instance Prodi dan menyimpan ke database
            prodi = Prodi(
                prodi_id=form.cleaned_data['prodi_id'],
                nama_prodi=form.cleaned_data['nama_prodi'],
                fakultas=form.cleaned_data['fakultas'],
                akreditasi=form.cleaned_data['akreditasi'],
                deskripsi=form.cleaned_data['deskripsi'],
                mata_kuliah_unggulan=[item.strip() for item in mata_kuliah_list],
                prospek_kerja=[item.strip() for item in prospek_kerja_list],
                url_resmi=form.cleaned_data['url_resmi'],
                gambar=file_url,  # Menyimpan URL gambar
            )
            prodi.save()

            return redirect('daftar_prodi')  # Redirect ke halaman prodi

    else:
        form = ProdiForm()

    return render(request, 'prodi/tambah_prodi.html', {'form': form})



def daftar_prodi(request):
    fakultas_terpilih = request.GET.get('fakultas')
    
    if fakultas_terpilih:
        prodis = Prodi.objects(fakultas=fakultas_terpilih)
    else:
        prodis = Prodi.objects()

    # Buat group by fakultas
    grouped = {}
    for prodi in prodis:
        grouped.setdefault(prodi.fakultas, []).append(prodi)

    # Daftar fakultas untuk dropdown
    semua_fakultas = Prodi.objects.distinct('fakultas')

    return render(request, 'prodi/daftar_prodi.html', {
        'grouped': grouped,
        'semua_fakultas': semua_fakultas,
        'fakultas_terpilih': fakultas_terpilih
    })


def tambah_fakultas(request):
    if request.method == 'POST':
        form = FakultasForm(request.POST, request.FILES)
        
        if form.is_valid():
            fakultas_id = form.cleaned_data['fakultas_id']
            nama = form.cleaned_data['nama']
            gambar = form.cleaned_data.get('gambar')

            # Mengecek apakah fakultas_id sudah ada
            if Fakultas.objects(fakultas_id=fakultas_id).first():
                form.add_error('fakultas_id', 'ID Fakultas sudah ada.')
            else:
                fakultas = Fakultas(
                    fakultas_id=fakultas_id,
                    nama=nama
                )

                # Menyimpan gambar jika ada
                if gambar:
                    # Menyimpan file gambar ke folder media
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    filename = fs.save(gambar.name, gambar)
                    file_url = fs.url(filename)

                    # Menyimpan path gambar ke dalam database
                    fakultas.gambar = file_url

                fakultas.save()

                return redirect('daftar_fakultas')  # Ubah dengan URL tujuan setelah berhasil
    else:
        form = FakultasForm()

    return render(request, 'prodi/tambah_fakultas.html', {'form': form})

  
  
def daftar_fakultas(request):
    semua_fakultas = Fakultas.objects.all()
    return render(request, 'prodi/daftar_fakultas.html', {'fakultas_list': semua_fakultas})