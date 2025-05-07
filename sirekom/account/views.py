# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def register_view(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        asal = request.POST.get('asal')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Tambahkan proses simpan ke DB sesuai model kamu
        return redirect('login')  # Redirect ke halaman login
    return render(request, 'account/register.html')

def masuk_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Ganti sesuai nama route dashboard kamu
        else:
            messages.error(request, 'Email atau kata sandi salah.')

    return render(request, 'account/masuk.html')
