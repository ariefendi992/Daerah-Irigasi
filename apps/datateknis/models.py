from django.db import models
from apps.masterdata.models import DaerahIrigasiModel
from smart_selects.db_fields import ChainedForeignKey
from decimal import Decimal
import os
import datetime


# Create your models here.
# NOTE: PETA
def upload_to_jenis_peta(instance, filename):
    base, ext = os.path.splitext(filename)
    jenis = instance.jenis_peta.lower() if instance.jenis_peta else "lainnya"
    tanggal = datetime.datetime.now().strftime("%Y%m%d")
    new_file_name = f"{base}_{tanggal}{ext}"
    return f"data_teknis/peta/{jenis}/{new_file_name}"


class PetaDIModel(models.Model):
    JENIS_PETA_CHOICES = [
        ("", "-- Pilih --"),
        ("baku", "Baku"),
        ("potensial", "Potensial"),
        ("fungsional", "Fungsional"),
    ]

    jenis_peta = models.CharField(
        "Jenis Peta", max_length=20, choices=JENIS_PETA_CHOICES
    )
    nama_peta = models.CharField("Nama Peta", max_length=120)
    deskripsi = models.TextField("Deskripsi", blank=True, null=True)
    file_peta = models.FileField(
        "File Peta (PDF/IMG)", upload_to=upload_to_jenis_peta, blank=True, null=True
    )
    tgl_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Data Peta Daerah Irigasi"

    def __str__(self):
        return f"{self.nama_peta} - {self.jenis_peta}"


# NOTE : Sumber Air Irigasi
# Data Bendung
class BendungModel(models.Model):
    nama_bendung = models.CharField("Nama Bendung", max_length=200)
    koordinat = models.CharField("Koordinat", max_length=150)
    lokasi = models.CharField("Lokasi", max_length=200)
    sumber_air = models.CharField("Sumber Air", max_length=100)
    debit = models.CharField("Debit", max_length=50)
    luas_petak_dialiri = models.CharField("Luas Petak Dialiri", max_length=50)
    tinggi_bendung = models.CharField("Tinggi Bendung", max_length=20)
    lebar_bendung = models.CharField("Lebar Bendung", max_length=20)
    jenis_mercu = models.CharField("Jenis Mercu", max_length=32)
    tipe_kolam_olak = models.CharField("Tipe Kolam Olak", max_length=50)
    status_kepemilikan_aset = models.CharField("Status Kepemilikan Aset", max_length=60)
    status_operasi_pemeliharaan = models.CharField(
        "Status Operasi & Pemeliharaan", max_length=60, null=True, blank=True
    )
    th_pembangunan = models.CharField("Tahun Pembangunan", max_length=30)

    class Meta:
        verbose_name_plural = "Data Bendung"

    def __str__(self):
        return f"Nama Bendung : {self.nama_bendung}"


# data Embung
class EmbungModel(models.Model):
    nama_embung = models.CharField("Nama Embung", max_length=120)
    lokasi = models.CharField("Lokasi", max_length=120)

    class Meta:
        verbose_name_plural = "Data Embung"

    def __str__(self):
        return f"Nama Embung : {self.nama_embung}"


# data ketesediaan Air
"""
    Note : Data Ketersedian
"""


class KondisiKetersediaanModel(models.Model):
    nama_kondisi = models.CharField("Nama Kondisi", max_length=150)

    class Meta:
        verbose_name_plural = "Master Kondisi Ketersediaan Air"

    def __str__(self):
        return f"{self.nama_kondisi}"


class SubKondisiKetersediaanModel(models.Model):
    kondisi_ketersediaan_id = models.ForeignKey(
        KondisiKetersediaanModel, on_delete=models.CASCADE
    )
    nama_sub_kondisi = models.CharField("Nama Sub Kondisi", max_length=150)

    class Meta:
        verbose_name_plural = "Master Kondisi Ketersediaan Sub"


class KetersediaanAirModel(models.Model):
    NAMA_BULAN = (
        ("", "-- Pilih --"),
        ("01", "Jan"),
        ("02", "Feb"),
        ("03", "Mar"),
        ("04", "Apr"),
        ("05", "Mei"),
        ("06", "Jun"),
        ("07", "Jul"),
        ("08", "Agst"),
        ("09", "Sept"),
        ("10", "Okt"),
        ("11", "Nov"),
        ("12", "Des"),
    )

    NAMA_PERIODE = (
        ("", "-- Pilih --"),
        ("i", "I"),
        ("ii", "II"),
    )
    nama_das = models.CharField("Nama DAS", max_length=150)
    kondisi = models.ForeignKey(KondisiKetersediaanModel, on_delete=models.CASCADE)
    sub_kondisi = ChainedForeignKey(
        SubKondisiKetersediaanModel,
        chained_field="kondisi",
        chained_model_field="kondisi_ketersediaan_id",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
    )
    # sub_kondisi = models.ForeignKey(
    #     SubKondisiKetersediaanModel, on_delete=models.CASCADE
    # )
    bulan = models.CharField("Bulan", choices=NAMA_BULAN)
    periode = models.CharField("Periode", choices=NAMA_PERIODE)
    nilai = models.CharField("Nilai", max_length=12, null=True, blank=True)
    rata_rata_th = models.CharField("Rata-rata Tahunan", max_length=12)
    ket = models.CharField("Keterangan", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Data Ketersediaan Air"

    def __str__(self):
        return f"Nama Das {self.nama_das}"


class NeracaAirModel(models.Model):
    NAMA_BULAN = (
        ("", "-- Pilih --"),
        ("01", "Jan"),
        ("02", "Feb"),
        ("03", "Mar"),
        ("04", "Apr"),
        ("05", "Mei"),
        ("06", "Jun"),
        ("07", "Jul"),
        ("08", "Agst"),
        ("09", "Sept"),
        ("10", "Okt"),
        ("11", "Nov"),
        ("12", "Des"),
    )

    NAMA_PERIODE = (
        ("", "-- Pilih --"),
        ("i", "I"),
        ("ii", "II"),
    )

    SKENARIO = (
        ("", "-- Pilih --"),
        ("Kebutuhan Air", "Kebutuhan Air"),
        ("Kondisi Basah (Debit Air Cukup)", "Kondisi Basah (Debit Air Cukup)"),
        ("Kondisi Normal (Debit Air Normal)", "Kondisi Normal (Debit Air Normal)"),
        ("Kondisi Rendah (Debit Air Rendah)", "Kondisi Rendah (Debit Air Rendah)"),
    )

    skenario_neraca_air = models.CharField(
        "Skenario Neraca Air", choices=SKENARIO, max_length=150
    )
    bulan = models.CharField("Bulan", choices=NAMA_BULAN)
    periode = models.CharField("Periode", choices=NAMA_PERIODE)
    nilai = models.CharField("Nilai", max_length=12, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Data Neraca Air"

    def __str__(self):
        return f"{self.skenario_neraca_air}"


# NOTE: SKEMA
def upload_to_skema(instance, filename):
    base, ext = os.path.splitext(filename)
    print(f"Base => {base}")
    print(f"ext => {ext}")
    if instance.jenis_skema_id and instance.jenis_skema_id.nama_skema:
        folder_name = instance.jenis_skema_id.nama_skema.lower().replace(" ", "_")
    else:
        folder_name = "lainnya"
    tanggal = datetime.datetime.now().strftime("%Y%m%d")
    new_filename = f"{base}{tanggal}{ext}"

    return os.path.join("skema", folder_name, new_filename)


class JenisSkemaModel(models.Model):
    nama_skema = models.CharField("Nama Skema", max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nama_skema}"


class SkemaModel(models.Model):
    jenis_skema_id = models.ForeignKey(
        JenisSkemaModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Jenis Skema",
    )
    daerah_irigasi_id = models.ForeignKey(
        DaerahIrigasiModel, on_delete=models.CASCADE, null=True, blank=True
    )
    file_skema = models.FileField(
        "File Skema (PDF/IMG)", upload_to=upload_to_skema, blank=True, null=True
    )
    tgl_upload = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Data Skema"

    def __str__(self):
        return f"{self.jenis_skema_id.nama_skema}"


# NOTE : Jaringan Irigasi Utama
class JenisJaringanModel(models.Model):
    nama_jaringan = models.CharField("Nama Jaringan Irigasi", max_length=100)
    keterangan = models.CharField(
        "Keterangan", max_length=120, null=True, blank=True, default="-"
    )

    def __str__(self):
        return f"{self.nama_jaringan}"


class JaringanPrimerModel(models.Model):
    jenis_jaringan_id = models.ForeignKey(
        JenisJaringanModel,
        on_delete=models.CASCADE,
        verbose_name="Jenis Jaringan",
        default="1",
    )
    nama_bangunan = models.CharField("Nama Bangunan", max_length=100)
    saluran = models.CharField("Saluran/Ruas", max_length=100)
    panjang_saluran = models.DecimalField(
        "Panjang Saluran (M)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    th_pembuatan = models.CharField("Tahun Pembuatan/Rehab", max_length=12)

    class Meta:
        verbose_name_plural = "Data Jaringan Primer"

    def __str__(self):
        return f"{self.nama_bangunan}"

    @classmethod
    def total_panjang(cls):
        """Mengihtung total panjang saluran"""
        total = cls.objects.aggregate(total=models.Sum("panjang_saluran"))["total"]
        return total or 0


class JaringanSekunderModel(models.Model):
    jenis_jaringan_id = models.ForeignKey(
        JenisJaringanModel,
        on_delete=models.CASCADE,
        verbose_name="Jenis Jaringan",
        default="2",
    )
    nama_bangunan = models.CharField("Nama Bangunan", max_length=100)
    saluran = models.CharField("Saluran/Ruas", max_length=100)
    panjang_saluran = models.DecimalField(
        "Panjang Saluran (m)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    th_pembuatan = models.CharField("Tahun Pembuatan/Rehab", max_length=12)

    class Meta:
        verbose_name_plural = "Data Jaringan Sekunder"

    def __str__(self):
        return f"{self.nama_bangunan}"

    @classmethod
    def total_panjang(cls):
        """Mengihtung total panjang saluran"""
        total = cls.objects.aggregate(total=models.Sum("panjang_saluran"))["total"]
        return total or 0


class JaringanTersierModel(models.Model):
    jenis_jaringan_id = models.ForeignKey(
        JenisJaringanModel,
        on_delete=models.CASCADE,
        verbose_name="Jenis Jaringan",
        default="3",
    )
    nama_bangunan = models.CharField("Nama Bangunan", max_length=100)
    nama_petak = models.CharField("Nama Petak Tersier", max_length=100)
    luasan = models.DecimalField(
        "Luasan (HA)", max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Data Jaringan Tersier"

    def __str__(self):
        return f"{self.nama_bangunan}"

    @classmethod
    def total_luasan(cls):
        """Mengihtung total luasan"""
        total = cls.objects.aggregate(total=models.Sum("luasan"))["total"]
        return total or 0


# NOTE: Petugas OP
# Jabatan Petugas
class JabatanPetugasOPModel(models.Model):
    JABATAN_PETUGAS_CHOICE = [
        ("", "-- Pilih --"),
        ("Pengamat", "Pengamat"),
        ("Mantri/Juru", "Mantri/Juru"),
        ("Petugas Pintu Air (PPA)", "Petugas Pintu Air (PPA)"),
        ("Petugas Operasi Bendu (POB)", "Petugas Operasi Bendu (POB)"),
    ]
    nama_jabatan = models.CharField(
        "Jabatan", max_length=100, choices=JABATAN_PETUGAS_CHOICE
    )

    def __str__(self):
        return self.nama_jabatan


class WilayahKerjaPetugasOPModel(models.Model):
    wilayah_kerja = models.CharField("Wilayah Kerja", max_length=80)
    daerah_irigasi_id = models.ForeignKey(
        DaerahIrigasiModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Daerah Irigasi",
    )

    def __str__(self):
        return self.wilayah_kerja


class PetugasOPModel(models.Model):
    nama_petugas = models.CharField("Nama Petugas", max_length=150)
    jabatan_id = models.ForeignKey(
        JabatanPetugasOPModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Jabatan",
    )
    # wilayah_kerja
    wilayah_kerja = models.ManyToManyField(
        WilayahKerjaPetugasOPModel, related_name="petugas_op", blank=True
    )

    class Meta:
        verbose_name_plural = "Data Petugas OP"

    def __str__(self):
        return f"{self.nama_petugas}"
