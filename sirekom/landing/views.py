from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Selamat datang di toko online!")

def index(request):
  return render(request, 'landing/landing.html')


# views.py
# from django.http import JsonResponse
# from .models import Produk

# def get_produk(request):
#     produk_list = Produk.objects.all()
#     data = [{"nama": p.nama, "harga": p.harga} for p in produk_list]
#     return JsonResponse({"produk": data})
