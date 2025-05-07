from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('masuk/', views.masuk_view, name="masuk"),
    path('keluar/', views.keluar_view, name='keluar'),
]