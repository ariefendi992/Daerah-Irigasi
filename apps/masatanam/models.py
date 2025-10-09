from django.db import models


# Create your models here.
class ProduktivitasPadiModel(models.Model):
    TINGKAT_CHOICES = [
        ("nasional", "Nasional"),
        ("provinsi", "Provinsi"),
        ("kabupaten", "Kabupaten"),
    ]

    th = models.PositiveBigIntegerField("Tahun Data", null=True, blank=True)
    tingkat_data = models.CharField(
        "Tingkat Data", max_length=20, choices=TINGKAT_CHOICES
    )
    sumber_data = models.CharField("Sumber Data", max_length=150, blank=True, null=True)
    produktivitas_rata_nasional = models.DecimalField(
        "Produktivitas Rata-rata Nasional (Ton/Ha)",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    produktivitas_daerah = models.DecimalField(
        "Produktivitas Daerah (Ton/Ha)",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    presentase = models.DecimalField(
        "Presentase Produktivitas (%)",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    wilayah = models.CharField("Nama Wilayah", max_length=100, blank=True, null=True)
    link_sumber = models.URLField(
        "Link Sumber Data", max_length=300, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        """Hitung otomatis presentase sebelum disimpan"""
        if self.produktivitas_rata_nasional > 0:
            hasil = (self.produktivitas_daerah / self.produktivitas_rata_nasional) * 100
            self.presentase = min(hasil, 100)  # Jika lebih dari 100%, tulis 100%
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Produktivitas Padi"
        ordering = ["-th", "wilayah"]

    def __str__(self):
        wilayah = self.wilayah or "Nasional"
        return f"Produktivitas Padi {wilayah} - {self.th}"


# NOTE: Realisasi Luas Tanam
class RealisasiLuasTanamModel(models.Model):
    """Model Realisasi Luas Tanam
    - [x] MT (Musim Tanam)
         ex. MT I, MT II, MT III
    """

    th = models.PositiveBigIntegerField("Tahun Data", null=True, blank=True)
    luas_potensial = models.DecimalField(
        "Luas Potensial (Ha)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    mt1 = models.DecimalField(
        "MT I (Ha)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    mt2 = models.DecimalField(
        "MT II (Ha)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    mt3 = models.DecimalField(
        "MT III (Ha)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    area_tanam = models.DecimalField(
        "Total Area Tanam (Ha)", max_digits=10, decimal_places=2, blank=True, null=True
    )
    ip_maks = models.DecimalField(
        "Indeks Pertanaman (IP) Maks (%)",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    ip_ada = models.DecimalField(
        "Indeks Pertanaman (IP) Yang Ada (%)",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    persen_realisasi = models.DecimalField(
        "Presentase Realisasi Luas Tanam (%)",
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    sumber_data = models.CharField("Sumber Data", max_length=150, null=True, blank=True)
    link_sumber = models.URLField("Link Sumber", max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = "Realisasi Luas Tanam"
        verbose_name_plural = "Realisasi Luas Tanam"
        ordering = ["-th"]

    def save(self, *args, **kwargs):
        """Hitung otomatis area tanam, IP, dan presentase"""
        self.area_tanam = (self.mt1 or 0) + (self.mt2 or 0) + (self.mt3 or 0)

        if self.luas_potensial > 0:
            # IP yang ada = (Area Tanam / Luas Potensial) * 100
            self.ip_ada = (self.area_tanam / self.luas_potensial) * 100

            # Presentase Realisati Luas Tanam = (IP Ada / IP Maks) * 100
            self.persen_realisasi = (
                (self.ip_ada / self.ip_maks) * 100 if self.ip_maks > 0 else 0
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Realisasi Luas Tanam {self.th}"
