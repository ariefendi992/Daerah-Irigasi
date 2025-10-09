from django.db import models
from uuid import uuid4
from apps.masterdata.models import DaerahIrigasiModel
import os


# Create your models here.
# NOTE: Peta Administrasi Distrik Oransbari


class JenisPetaPengembanganDIModel(models.Model):
    nama_jenis_peta = models.CharField(
        "Nama Jenis Peta", max_length=150, null=True, blank=True
    )

    def __str__(self):
        return self.nama_jenis_peta


def upload_to_pengembangan(instance, filename):
    ext = filename.split(".")[-1]

    if instance.jenis_peta_id:
        jenis_peta = instance.jenis_peta_id.nama_jenis_peta or "lainnya"
        c_jenis_peta = "_".join(jenis_peta.split(" ")).lower()
    else:
        c_jenis_peta = "tanpa_jenis"
    new_filename = f"{uuid4().hex}_{c_jenis_peta}.{ext}"

    return os.path.join("pengembangan_di/", new_filename)


class PengembanganDaerahIrigasiModel(models.Model):
    daerah_irigasi_id = models.ForeignKey(
        DaerahIrigasiModel, on_delete=models.CASCADE, verbose_name="Nama Daerah Irigasi"
    )
    jenis_peta_id = models.ForeignKey(
        JenisPetaPengembanganDIModel, on_delete=models.CASCADE, null=True, blank=True
    )
    sumber_data = models.CharField("Sumber Data", max_length=200, blank=True, null=True)
    keterangan = models.TextField("Ket. Tambahan", blank=True, null=True)
    tgl_upload = models.DateTimeField("Tanggal Upload", auto_now_add=True)
    file_peta = models.FileField(
        "File Peta", upload_to=upload_to_pengembangan, blank=True, null=True
    )

    class Meta:
        verbose_name = "Pengembangan Daerah Irigasi"
        verbose_name_plural = "Pengembangan Daerah Irigasi"
        ordering = ["-tgl_upload"]

    def __str__(self):
        return f"{self.daerah_irigasi_id.nama_irigasi} - {self.tgl_upload.strftime('$d-%m-%Y')}"
