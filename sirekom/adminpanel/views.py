from django.shortcuts import render, redirect
from account.decorators import admin_required
from prodi.models import Prodi 
from .forms import ProdiForm 
from account.models import CustomUser  # model user kamu
from prodi.models import Fakultas     # model lain yang kamu butuh
from math import ceil
from django.http import Http404
from mongoengine.queryset.visitor import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Create your views here.
@admin_required
def dashboard_admin(request):
    
    user_id = request.session.get('user_id')
    
    if not user_id:
        # Jika tidak ada user_id dalam session, arahkan ke login
        return redirect('login')

    # Ambil data user berdasarkan user_id dari session
    user = CustomUser.objects.get(id=user_id)

    # Ambil data fakultas atau prodi yang sesuai dengan user (sesuaikan dengan kebutuhan)
    # Misalnya, jika setiap user memiliki fakultas tertentu
    semua_fakultas = Fakultas.objects.all()

    return render(request, 'adminpanel/dashboard.html', {
        'fakultas_list': semua_fakultas,
        'user': user
    })
    


def daftar_pengguna(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)

    query = request.GET.get('query', '')  # Ambil keyword pencarian dari URL
    if query:
        semua_user = CustomUser.objects.filter(
            Q(nama__icontains=query) |
            Q(email__icontains=query) |
            Q(sekolah_asal__icontains=query)
        )
    else:
        semua_user = CustomUser.objects.all()

    total_data = semua_user.count()
    items_per_page = 5  
    total_pages = ceil(total_data / items_per_page)
    page_numbers = list(range(1, total_pages + 1))

    return render(request, 'adminpanel/daftar_pengguna.html', {
        'pengguna': semua_user,
        'user': user,
        'page_numbers': page_numbers
    })


def hapus_pengguna(request, user_id):
    try:
        pengguna = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        raise Http404("Pengguna tidak ditemukan.")
    
    pengguna.delete()
    return redirect('daftar_pengguna')
    
from math import ceil

from django.core.paginator import Paginator

def daftar_prodi(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = CustomUser.objects.get(id=user_id)
    
    query = request.GET.get('query', '')
    page_number = request.GET.get('page', 1)
    
    if query:
        prodi_list = Prodi.objects.filter(nama_prodi__icontains=query)
    else:
        prodi_list = Prodi.objects.all()

    paginator = Paginator(prodi_list, 5)  # 7 data per halaman
    page_obj = paginator.get_page(page_number)

    offset = (page_obj.number - 1) * paginator.per_page

    context = {
        'user': user,
        'prodi': page_obj,
        'page_numbers': paginator.page_range,
        'query': query,
        'offset': offset,
    }
    return render(request, 'adminpanel/daftar_prodi.html', context)


from mongoengine.errors import DoesNotExist
from django.contrib import messages

def hapus_prodi(request, prodi_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        prodi = Prodi.objects.get(id=prodi_id)
        prodi.delete()
        messages.success(request, "Program studi berhasil dihapus.")
    except DoesNotExist:
        messages.error(request, "Program studi tidak ditemukan.")

    return redirect('daftar_prodi')


from django.core.files.storage import FileSystemStorage
from django.conf import settings

def edit_prodi(request, prodi_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    user = CustomUser.objects.get(id=user_id)
    prodi = Prodi.objects(prodi_id=prodi_id).first()

    if not prodi:
        messages.error(request, "Program studi tidak ditemukan.")
        return redirect('daftar_prodi')

    if request.method == 'POST':
        form = ProdiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(prodi=prodi)  # Perhatikan: method `save()` sudah menangani file gambar
            messages.success(request, "Program studi berhasil diperbarui.")
            return redirect('daftar_prodi')
    else:
        # Pre-fill data lama dari MongoDB
        initial_data = {
            'nama_prodi': prodi.nama_prodi,
            'fakultas': str(prodi.fakultas.fakultas_id) if prodi.fakultas else '',
            'akreditasi': prodi.akreditasi,
            'deskripsi': prodi.deskripsi,
            'mata_kuliah_unggulan': ', '.join(prodi.mata_kuliah_unggulan),
            'prospek_kerja': ', '.join(prodi.prospek_kerja),
            'url_resmi': prodi.url_resmi,
        }
        form = ProdiForm(initial=initial_data)

    return render(request, 'adminpanel/edit_prodi.html', {
        'form': form,
        'user': user,
        'prodi': prodi,  # penting agar gambar lama bisa diakses di template
    })


