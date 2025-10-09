from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class DaerahIrigasiModel(models.Model):
    nama_irigasi = models.CharField("Nama D.I.", max_length=150)
    lokasi = models.CharField("Lokasi", max_length=150)

    class Meta:
        verbose_name_plural = "Data Daerah Irigasi"

    def __str__(self):
        return f"{self.nama_irigasi}"


# NOTE Sumber Air Irigasi
class SumberAirigasiModel(models.Model):
    """Abstrak atau hanya tampil untuk di arahkan ke selengkapnya"""

    nama_sumber_air = models.CharField("Nama Sumber Air", max_length=150)
    selengkap_url = models.URLField("Url Detail", max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = "Sumber Air Irigasi"
        verbose_name_plural = "Sumber Air Irigasi"

    def __str__(self):
        return self.nama_sumber_air


# NOTE: DATA UMUM
class DataUmuModel(models.Model):
    daerah_irigasi_id = models.ForeignKey(
        DaerahIrigasiModel, on_delete=models.CASCADE, verbose_name="Nama Irigasi"
    )
    deskripsi = RichTextField("Deskripsi", null=True, blank=True)
    created_at = models.DateTimeField("Tgl Posting", auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Data Umum"
        verbose_name_plural = "Data Umum"

    def __str__(self):
        return self.daerah_irigasi_id.nama_irigasi


# NOTE: Saluran Irgiasi
class TipeSaluranModel(models.Model):
    nama_tipe = models.CharField(
        "Nama Tipe Saluran", max_length=120, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Master Tipe Saluran"

    def __str__(self):
        return f"Tipe Saluran {self.nama_tipe}"


class KondisiSaluranModel(models.Model):
    nama_kondisi = models.CharField(
        "Nama Kondisi Saluran", max_length=120, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Master Kondisi Saluran"

    def __str__(self):
        return f"Kondisi Saluran {self.nama_kondisi}"


class JenisBangunanModel(models.Model):
    nama_jenis = models.CharField(
        "Jenis Bangunan", max_length=200, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Master Jenis Bangunan"

    def __str__(self):
        return f"Jenis Bangunan {self.nama_jenis}"


class SaluranModel(models.Model):
    nama_saluran = models.CharField("Nama Saluran", max_length=200)
    tipe_id = models.ForeignKey(
        TipeSaluranModel, on_delete=models.CASCADE, null=True, blank=True
    )
    panjang_saluran = models.CharField("Panjang", max_length=4, null=True, blank=True)
    kondisi_id = models.ForeignKey(
        KondisiSaluranModel, on_delete=models.CASCADE, null=True, blank=True
    )
    koordinat_start = models.CharField(
        "Koordinat Start", max_length=100, null=True, blank=True
    )
    koordinat_end = models.CharField(
        "Koordinat end", max_length=100, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Data Saluran Irigasi"

    def __str__(self):
        return f"Nama Saluran {self.nama_saluran}"


class BangunanModel(models.Model):
    saluran_id = models.ForeignKey(
        SaluranModel, on_delete=models.CASCADE, null=True, blank=True
    )
    nama_bangunan = models.CharField(
        "Nama Bangunan", max_length=200, null=True, blank=True
    )
    jenis = models.ForeignKey(
        JenisBangunanModel, on_delete=models.CASCADE, null=True, blank=True
    )
    kondisi = models.CharField("Kondisi", max_length=100, null=True, blank=True)
    koordinat = models.CharField("Koordinat", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Data Bangunan Irigasi"

    def __str__(self):
        return f"Nama Bangungan {self.nama_bangunan}"


class PetakModel(models.Model):
    saluran_id = models.ForeignKey(
        SaluranModel, on_delete=models.CASCADE, null=True, blank=True
    )
    luas = models.CharField("Luas", max_length=20, null=True, blank=True)
    desa = models.CharField("Desa", max_length=200, null=True, blank=True)
    kelompok_tani = models.CharField(
        "Kelompok Tani", max_length=200, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Data Petak"

    def __str__(self):
        return f"Petak Model {self.id_saluran}"
