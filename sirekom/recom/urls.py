from django.urls import path
from . import views

urlpatterns = [
    path('instruksi/', views.instruksi_view, name="instruksi"),
]