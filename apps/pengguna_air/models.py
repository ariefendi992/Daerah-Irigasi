from django.db import models


# Create your models here.
class P3AModel(models.Model):
    nama_p3a = models.CharField("Nama P3A", max_length=100)
    desa = models.CharField("Desa")
    jumlah_anggota = models.CharField("Jumlah Anggota")

    def __str__(self):
        return f"Nama P3A {self.nama_p3a}"


class AnggotaP3aModel(models.Model):
    p3a_id = models.ForeignKey(P3AModel, on_delete=models.CASCADE)
    nama = models.CharField("Nama Anggota", max_length=200)
    luas_garapan = models.CharField("Luas Garapan (ha)", max_length=20)
    komoditas = models.CharField("Komoditas", max_length=200)

    def __str__(self):
        return f"Nama Anggota {self.nama}"
