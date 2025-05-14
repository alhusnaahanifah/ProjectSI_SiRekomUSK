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
from django.contrib import messages
from account.decorators import siswa_required
from account.models import CustomUser
from django.http import Http404
from django.urls import reverse
from account.decorators import admin_required
from .models import Testimoni
from .forms import TestimoniForm

# Create your views here.
@siswa_required
def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)
    semua_fakultas = Fakultas.objects.all()

    if request.method == 'POST' and 'submit_testimoni' in request.POST:
        testimoni_form = TestimoniForm(request.POST)
        if testimoni_form.is_valid():
            testimoni = Testimoni(
                user=user,
                nama=testimoni_form.cleaned_data['nama'],
                isi=testimoni_form.cleaned_data['isi']
            )
            testimoni.save()
            messages.success(request, "Testimoni berhasil dikirim!")
            return redirect('dashboard_siswa')
    else:
        # Set nilai awal untuk nama
        initial_data = {'nama': user.nama}
        testimoni_form = TestimoniForm(initial=initial_data)

    return render(request, 'prodi/dashboard.html', {
        'fakultas_list': semua_fakultas,
        'user': user,
        'testimoni_form': testimoni_form,
    })

@admin_required
def tambah_prodi(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Jika tidak ada user_id dalam session, arahkan ke login
        return redirect('login')

    # Ambil data user berdasarkan user_id dari session
    user = CustomUser.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = ProdiForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            # Cek apakah prodi_id sudah ada
            if Prodi.objects(prodi_id=data['prodi_id']).first():
                form.add_error('prodi_id', 'ID Prodi sudah ada.')
            else:
                # Ambil objek Fakultas
                fakultas_obj = Fakultas.objects(fakultas_id=data['fakultas']).first()
                if not fakultas_obj:
                    form.add_error('fakultas', 'Fakultas tidak ditemukan.')
                else:
                    # Upload gambar jika ada
                    gambar = None
                    if 'gambar' in request.FILES:
                        uploaded_file = request.FILES['gambar']
                        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                        filename = fs.save(uploaded_file.name, uploaded_file)
                        gambar = fs.url(filename)
                        
                        mata_kuliah_list = form.cleaned_data['mata_kuliah_unggulan'].split(',')
                        prospek_kerja_list = form.cleaned_data['prospek_kerja'].split(',')
                        
                    # Buat dan simpan objek Prodi
                    prodi = Prodi(
                        prodi_id=data['prodi_id'],
                        nama_prodi=data['nama_prodi'],
                        fakultas=fakultas_obj,
                        akreditasi=data.get('akreditasi'),
                        deskripsi=data.get('deskripsi'),
                        mata_kuliah_unggulan=[item.strip() for item in mata_kuliah_list],
                        prospek_kerja=[item.strip() for item in prospek_kerja_list],
                        url_resmi=data.get('url_resmi'),
                        gambar=gambar,
                    )
                    prodi.save()
                    messages.success(request, "Prodi berhasil ditambahkan.")
                    return redirect('daftar_prodi')
    else:
        form = ProdiForm()

    return render(request, 'prodi/tambah_prodi.html', {'form': form, 'user':user })


def daftar_prodi(request):
    semua_prodi = Prodi.objects.select_related()
    return render(request, 'prodi/daftar_prodi.html', {'prodi_list': semua_prodi})


@admin_required
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

  
@admin_required  
def daftar_fakultas(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Jika tidak ada user_id dalam session, arahkan ke login
        return redirect('login')

    # Ambil data user berdasarkan user_id dari session
    user = CustomUser.objects.get(id=user_id)
    semua_fakultas = Fakultas.objects.all()
    return render(request, 'prodi/daftar_fakultas.html', {'fakultas_list': semua_fakultas, 'user': user})

@admin_required
def edit_fakultas(request, fakultas_id):
    fakultas = Fakultas.objects(fakultas_id=fakultas_id).first()
    if not fakultas:
        raise Http404("Fakultas tidak ditemukan.")

    if request.method == 'POST':
        form = FakultasForm(request.POST, request.FILES, initial=fakultas.to_mongo().to_dict())
        if form.is_valid():
            fakultas.nama = form.cleaned_data['nama']

            gambar = form.cleaned_data.get('gambar')
            if gambar:
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(gambar.name, gambar)
                file_url = fs.url(filename)
                fakultas.gambar = file_url

            fakultas.save()
            return redirect('daftar_fakultas')
    else:
        form = FakultasForm(initial={
            'fakultas_id': fakultas.fakultas_id,
            'nama': fakultas.nama,
        })

    return render(request, 'prodi/edit_fakultas.html', {'form': form, 'fakultas': fakultas})

@admin_required
def hapus_fakultas(request, fakultas_id):
    fakultas = Fakultas.objects(fakultas_id=fakultas_id).first()
    if not fakultas:
        raise Http404("Fakultas tidak ditemukan.")

    fakultas.delete()
    return redirect('daftar_fakultas')


def detail_prodi(request, fakultas_id):
    try:
        fakultas = Fakultas.objects.get(id=fakultas_id)
    except Fakultas.DoesNotExist:
        raise Http404("Fakultas tidak ditemukan")

    daftar_prodi = Prodi.objects(fakultas=fakultas)
    
    return render(request, 'prodi/detail_prodi.html', {
        'fakultas': fakultas,
        'daftar_prodi': daftar_prodi,
    })