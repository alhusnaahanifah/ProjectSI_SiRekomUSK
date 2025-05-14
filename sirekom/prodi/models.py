from django.db import models
from account.models import CustomUser 

# Create your models here.
from mongoengine import Document, StringField, ListField, ReferenceField

class Fakultas(Document):
    fakultas_id = StringField(required=True, unique=True)
    nama = StringField(required=True, unique=True)
    gambar = StringField()  # path gambar/logo fakultas

class Prodi(Document):
    prodi_id = StringField(required=True, unique=True)
    nama_prodi = StringField(required=True)
    fakultas = ReferenceField(Fakultas, required=True)
    akreditasi = StringField()
    deskripsi = StringField()
    mata_kuliah_unggulan = ListField(StringField())
    prospek_kerja = ListField(StringField())
    url_resmi = StringField()
    gambar = StringField()  # Simpan path ke file image
    
class Testimoni(Document):
    user = ReferenceField(CustomUser, required=True)
    nama = StringField()
    isi = StringField(required=True)
