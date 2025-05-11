from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('register/', views.register_siswa, name="register"),
    path('login/', views.login_siswa, name='login'),
    path('keluar/', views.logout_view, name='keluar'),
]

# path('masuk/', views.masuk_view, name="masuk"),
# path('keluar/', views.keluar_view, name='keluar'),
# path('register1/', views.register_siswa, name='register_siswa'),