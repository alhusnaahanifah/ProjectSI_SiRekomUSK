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
            print(request.POST)

            return redirect('login')  # sesuaikan
    else:
        form = SiswaRegisterForm()

    return render(request, 'account/register.html', {'form': form})

def login_siswa(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next')  # Tangkap dari hidden input

        try:
            user = CustomUser.objects.get(email=email)
            if user and check_password(password, user.password):
                # Simpan session
                request.session['user_id'] = str(user.id)
                request.session['user_email'] = user.email
                request.session['is_admin_custom'] = user.is_admin_custom
                request.session['is_siswa'] = user.is_siswa
                request.session['user_nama'] = user.nama

                # ✅ Redirect berdasarkan role
                if next_url:
                    return redirect(next_url)  # redirect ke halaman sebelum login
                elif user.is_admin_custom:
                    return redirect('dashboard_admin')
                elif user.is_siswa:
                    return redirect('dashboard_siswa')
            else:
                messages.error(request, 'Email atau password salah!')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Akun tidak ditemukan.')

    # Kirim nilai `next` ke template agar tetap terisi di form login
    return render(request, 'account/masuk.html', {'next': request.GET.get('next', '')})


def logout_view(request):
    request.session.flush()  # Hapus semua data session
    return redirect('login')

