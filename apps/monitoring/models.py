from django.db import models
from apps.masterdata.models import SaluranModel, BangunanModel, PetakModel


# Create your models here.
class MonitoringSaluranModel(models.Model):
    saluran_id = models.ForeignKey(SaluranModel, on_delete=models.CASCADE)
    tanggal_monitoring = models.DateField("Tanggal Monitoring")
    jam_monitoring = models.TimeField("Jam Monitoring")
    debit_terukur = models.CharField("Debit Terukur (Liter/Detik)", max_length=12)
    kondisi = models.CharField("Kondisi", max_length=60)
    catatan = models.TextField("Catatan")
    foto_url = models.TextField("Url Foto", max_length=255)

    def __str__(self):
        return f"Tanggal monitoring Saluran {self.tanggal_monitoring}"


class MonitoringBangunanModel(models.Model):
    FUNGSI_SELECT = (
        ("", "-- Pilih --"),
        ("berfungsi", "Berfungsi"),
        ("tidak_berfungsi", "Tidak Berfungsi"),
    )
    bangunan_id = models.ForeignKey(
        BangunanModel, on_delete=models.CASCADE, null=True, blank=True
    )
    tanggal_monitoring = models.DateField("Tanggal Monitoring")
    jam_monitoring = models.TimeField("Jam Monitoring")
    catatan = models.TextField("Catatan")
    foto_url = models.TextField("Url Foto", max_length=255)

    def __str__(self):
        return f"Tanggal monitoring Bangunan {self.tanggal_monitoring}"


class MonitoringPetakModel(models.Model):
    petak_id = models.ForeignKey(PetakModel, on_delete=models.CASCADE)
    tanggal_monitoring = models.DateField("Tanggal Monitoring")
    jam_monitoring = models.TimeField("Jam Monitoring")
    luas_terairi = models.CharField("Luas Terairi (ha)", max_length=12)
    catatan = models.TextField("Catatan")

    def __str__(self):
        return f"Tanggal monitoring Petak {self.tanggal_monitoring}"


# Monitoring Masa Tanam
# Monitoring neraca air