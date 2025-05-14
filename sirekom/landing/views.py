from django.shortcuts import render
from django.http import HttpResponse
from prodi.models import Testimoni


def index(request):
    testimonials = Testimoni.objects.all().order_by('-id')[:3]
    print(f"Testimoni ditemukan: {testimonials}")  # Debug lebih detail
    return render(request, 'landing/landing.html', {
        'testimonials': testimonials,
        'debug_mode': True  # Untuk memudahkan debugging di template
    })
