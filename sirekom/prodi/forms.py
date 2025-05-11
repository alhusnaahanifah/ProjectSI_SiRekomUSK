from django import forms
from .models import Fakultas

FAKULTAS_CHOICES = [
    ('Fakultas Teknik', 'Fakultas Teknik'),
    ('Fakultas Ekonomi', 'Fakultas Ekonomi'),
    ('Fakultas Kedokteran', 'Fakultas Kedokteran'),
    ('Fakultas Hukum', 'Fakultas Hukum'),
]

class FakultasForm(forms.Form):
    fakultas_id = forms.CharField(
        label="ID Fakultas", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'contoh: TI001'})
    )
    nama = forms.CharField(label='Nama Fakultas', max_length=100)
    gambar = forms.ImageField(label='Logo Fakultas', required=False)   

class ProdiForm(forms.Form):
    prodi_id = forms.CharField(
        label="ID Prodi", 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'contoh: TI001'})
    )

    nama_prodi = forms.CharField(
        label="Nama Program Studi", 
        max_length=200
    )
    
    fakultas = forms.CharField(label="ID Fakultas")  # ID, bukan object

    akreditasi = forms.CharField(
        label="Akreditasi", 
        max_length=15
    )

    deskripsi = forms.CharField(
        label="Deskripsi", 
        widget=forms.Textarea(attrs={'rows': 3})
    )

    mata_kuliah_unggulan = forms.CharField(
        label="Mata Kuliah Unggulan",
        help_text="Pisahkan dengan koma, contoh: AI, Data Mining, Jaringan"
    )

    prospek_kerja = forms.CharField(
        label="Prospek Kerja",
        help_text="Pisahkan dengan koma, contoh: Programmer, Data Analyst"
    )

    url_resmi = forms.URLField(
        label="URL Resmi", 
        required=False
    )
    
    gambar = forms.ImageField(label="Logo Prodi", required=False)

