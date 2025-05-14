from django import forms
from mongoengine import QuerySet
from prodi.models import Prodi, Fakultas
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


class ProdiForm(forms.Form):
    nama_prodi = forms.CharField(max_length=255)
    fakultas = forms.ChoiceField(choices=[])
    akreditasi = forms.CharField(required=False)
    deskripsi = forms.CharField(widget=forms.Textarea, required=False)
    mata_kuliah_unggulan = forms.CharField(widget=forms.Textarea, required=False)
    prospek_kerja = forms.CharField(widget=forms.Textarea, required=False)
    url_resmi = forms.URLField(required=False)
    gambar = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(ProdiForm, self).__init__(*args, **kwargs)
        # Set fakultas choices berdasarkan data dari MongoDB
        fakultas_choices = [(str(fakultas.fakultas_id), fakultas.nama) for fakultas in Fakultas.objects]
        self.fields['fakultas'].choices = fakultas_choices

    def clean_mata_kuliah_unggulan(self):
        return [item.strip() for item in self.cleaned_data['mata_kuliah_unggulan'].split(',')]

    def clean_prospek_kerja(self):
        return [item.strip() for item in self.cleaned_data['prospek_kerja'].split(',')]

    def save(self, prodi=None):
        gambar_path = prodi.gambar if prodi else None  # default pakai gambar lama

        if self.files.get('gambar'):
            gambar_file = self.files['gambar']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(gambar_file.name, gambar_file)
            gambar_path = fs.url(filename)  # Simpan hanya nama file, bukan URL

        if prodi:
            prodi.update(
                nama_prodi=self.cleaned_data['nama_prodi'],
                fakultas=Fakultas.objects.get(fakultas_id=self.cleaned_data['fakultas']),
                akreditasi=self.cleaned_data.get('akreditasi'),
                deskripsi=self.cleaned_data.get('deskripsi'),
                mata_kuliah_unggulan=self.cleaned_data['mata_kuliah_unggulan'],
                prospek_kerja=self.cleaned_data['prospek_kerja'],
                url_resmi=self.cleaned_data.get('url_resmi'),
                gambar=gambar_path  # gunakan path gambar yang benar
            )
        else:
            Prodi.objects.create(
                nama_prodi=self.cleaned_data['nama_prodi'],
                fakultas=Fakultas.objects.get(fakultas_id=self.cleaned_data['fakultas']),
                akreditasi=self.cleaned_data.get('akreditasi'),
                deskripsi=self.cleaned_data.get('deskripsi'),
                mata_kuliah_unggulan=self.cleaned_data['mata_kuliah_unggulan'],
                prospek_kerja=self.cleaned_data['prospek_kerja'],
                url_resmi=self.cleaned_data.get('url_resmi'),
                gambar=gambar_path
            )
