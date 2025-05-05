from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def index(request):
#     return HttpResponse("Selamat datang di toko online!")

def index(request):
  return render(request, 'landing/landing.html')