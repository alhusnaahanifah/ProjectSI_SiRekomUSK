from django import forms

class SiswaRegisterForm(forms.Form):
    nama = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    sekolah_asal = forms.CharField(max_length=100)
    jenis_kelamin = forms.ChoiceField(choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])