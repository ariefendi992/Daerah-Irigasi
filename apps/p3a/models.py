from django.db import models


# Create your models here.
class PetakTersierModel(models.Model):
    """Detail Petak Tersier per P3A"""

    nama_petak = models.CharField("Nama Petak", max_length=100)
    nomenklatur = models.CharField("Nomenklatur", max_length=100, null=True, blank=True)
    luas = models.DecimalField(
        "Luas (Ha)", max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Petak Tersier"

    def __str__(self):
        return f"{self.nama_petak} ({self.luas} Ha)"


class P3AModel(models.Model):
    """Data utama P3A/GP3A/IP3A"""

    nama_p3a = models.CharField("Nama P3A/GP3A/IP3A", max_length=150)
    desa = models.CharField("Desa", max_length=100)
    kecamatan = models.CharField("Kecamatan", max_length=100)
    kabupaten = models.CharField("Kabupaten", max_length=100)
    luas_area_fungsional = models.DecimalField(
        "Luas Area Fungsional (Ha)", max_digits=10, decimal_places=2
    )
    bangunan_pengambilan = models.CharField(
        "Bangunan Pengambilan", max_length=150, null=True, blank=True
    )
    # petak_tersier = models.ManyToManyField(
    #     PetakTersierModel,
    #     verbose_name="Petak Tersier",
    #     blank=True,
    #     related_name="p3a_terkait",
    # )
    sk_bupati = models.CharField("SK Bupati", max_length=100, null=True, blank=True)
    akta_notaris = models.CharField(
        "Akta Notaris", max_length=150, null=True, blank=True
    )
    th_legalitas = models.CharField(
        "Tahun Legalitas", max_length=10, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Data Wilayah Kerja P3A/GP3A/IP3A"

    def __str__(self):
        return f"{self.nama_p3a}"

    @property
    def total_luas_petak(self):
        """Menjumlahkan luas semua petak tersier terkait"""
        total = self.petak_tersier.aggregate(models.Sum("luas"))["luas__sum"]

        return total or 0


# Relasi One-to-Many: Petak tersier milik satu P3A
PetakTersierModel.add_to_class(
    "p3a",
    models.ForeignKey(P3AModel, on_delete=models.CASCADE, related_name="petak_tersier"),
)
