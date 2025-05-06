# views.py
from django.shortcuts import render, redirect

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
