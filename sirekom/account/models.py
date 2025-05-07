from django.db import models

# Create your models here.
# account/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    asal_sekolah = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=20, choices=[('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan')])
