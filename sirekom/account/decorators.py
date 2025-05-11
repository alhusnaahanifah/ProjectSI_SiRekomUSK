from django.shortcuts import redirect

def siswa_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_siswa'):
            return view_func(request, *args, **kwargs)
        return redirect('login')  # Atau halaman akses ditolak
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_admin_custom'):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper
