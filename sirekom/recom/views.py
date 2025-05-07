from django.shortcuts import render

# Create your views here.
def instruksi_view(request):
    return render(request, 'recom/instruksi.html')