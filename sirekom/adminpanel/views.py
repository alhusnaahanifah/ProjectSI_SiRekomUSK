from django.shortcuts import render, redirect
from account.decorators import admin_required
from account.models import CustomUser  # model user kamu
from prodi.models import Fakultas     # model lain yang kamu butuh


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
        # Jika tidak ada user_id dalam session, arahkan ke login
        return redirect('login')

    # Ambil data user berdasarkan user_id dari session
    user = CustomUser.objects.get(id=user_id)
    
    semua_user = CustomUser.objects.all()

    return render(request, 'adminpanel/daftar_pengguna.html', {
        'pengguna': semua_user,
        'user': user
    })
    