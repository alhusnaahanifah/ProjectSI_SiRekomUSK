# accounts/models.py
from mongoengine import Document, StringField, BooleanField

class CustomUser(Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    nama = StringField()
    is_siswa = BooleanField(default=False)
    is_admin_custom = BooleanField(default=False)

    meta = {'collection': 'user'}

    siswa_id = StringField()
    sekolah_asal = StringField()
    jenis_kelamin = StringField(choices=["Laki-laki", "Perempuan"])
