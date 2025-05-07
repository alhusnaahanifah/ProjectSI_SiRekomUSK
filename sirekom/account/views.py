# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        # misal ambil data dari form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Simpan data user (sesuaikan dengan model dan formmu)
        user = CustomUser.objects.create_user(full_name=full_name, email=email, password=password)

        # Tambahkan pesan sukses
        messages.success(request, 'Pendaftaran berhasil! Silakan login.')
        
        return redirect('masuk')  # sesuaikan dengan nama URL login

def masuk_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'account/masuk.html', {'form': form})

def keluar_view(request):
    logout(request)
    return redirect('masuk')
