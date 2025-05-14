from django.urls import path
from . import views

urlpatterns = [
    path('instruksi/', views.instruksi_view, name="instruksi"),
    path('rekomendasi/', views.rekomendasi, name="rekomendasi"),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/<int:page>/', views.quiz, name='quiz'),
]