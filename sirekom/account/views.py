# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password  # pastikan ini diimport
from django.contrib.auth.hashers import check_password
from .forms import SiswaRegisterForm
from .models import CustomUser

def register_siswa(request):
    if request.method == 'POST':
        form = SiswaRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Auto-generate siswa_id
            siswa_id = f"SISWA{CustomUser.objects.count() + 1:04}"

            # Enkripsi password dengan make_password
            encrypted_password = make_password(data['password'])

            # Simpan user ke MongoDB
            user = CustomUser(
                nama=data['nama'],
                email=data['email'],
                password=encrypted_password,  # gunakan password terenkripsi
                sekolah_asal=data['sekolah_asal'],
                jenis_kelamin=data['jenis_kelamin'],
                is_siswa=True,
                siswa_id=siswa_id
            )
            user.save()

            # NOTE: login() tidak langsung bekerja karena Django auth default pakai ORM
            # Kamu perlu handle session login manual atau pakai custom backend

            messages.success(request, 'Registrasi berhasil!')

            return redirect('login')  # sesuaikan
    else:
        form = SiswaRegisterForm()

    return render(request, 'account/register_siswa.html', {'form': form})


def login_siswa(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(email=email)
            if user and check_password(password, user.password):
                request.session['user_id'] = str(user.id)
                messages.success(request, 'Login berhasil!')
                return redirect('dashboard_siswa')
            else:
                messages.error(request, 'Email atau password salah.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Akun tidak ditemukan.')

    return render(request, 'account/masuk.html')
