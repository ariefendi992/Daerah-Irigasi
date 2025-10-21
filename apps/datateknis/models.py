from django.db import models
from apps.masterdata.models import DaerahIrigasiModel
from smart_selects.db_fields import ChainedForeignKey
from apps.akun.models import UserModel
from decimal import Decimal
from PIL import Image
from config import settings
import fitz
import os, io
import datetime


# Create your models here.
# NOTE: PETA
def upload_to_jenis_peta(instance, filename):
    base, ext = os.path.splitext(filename)
    jenis = instance.jenis_peta.lower() if instance.jenis_peta else "lainnya"
    tanggal = datetime.datetime.now().strftime("%Y%m%d")
    new_file_name = f"{base}_{tanggal}{ext}"
    return f"data_teknis/peta/{jenis}/{new_file_name}"


def upload_to_bendung(instance, filename):
    base, ext = os.path.splitext(filename)
    nama_bendung = instance.nama_bendung.lower()
    tanggal = datetime.datetime.now().strftime("%Y%m%d")
    new_file_name = f"{nama_bendung}_{tanggal}{ext}"
    return f"data_teknis/bendung/{new_file_name}"


def upload_to_embung(instance, filename):
    base, ext = os.path.splitext(filename)
    nama_embung = instance.nama_embung.lower()
    tanggal = datetime.datetime.now().strftime("%Y%m%d")
    new_file_name = f"{nama_embung}_{tanggal}{ext}"
    return f"data_teknis/embung/{new_file_name}"


def upload_to_ketersediaan_air(instance, filename):
    base, ext = os.path.splitext(filename)
    nama_file = instance.nama_dokumen.lower()
    tanggal = datetime.datetime.now().strftime("%Y%m%d")
    new_file_name = f"{nama_file}_{tanggal}{ext}"
    return f"data_teknis/ketersediaan_air/{new_file_name}"


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
        "File Peta (PDF)", upload_to=upload_to_jenis_peta, blank=True, null=True
    )
    preview_peta = models.ImageField(
        "Preview", upload_to=upload_to_jenis_peta, blank=True, null=True
    )
    tgl_upload = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file_peta and not self.preview_peta:
            if self.file_peta and not self.preview_peta:
                ext = os.path.splitext(self.file_peta.name)[1].lower()

                if ext in [".jpg", ",jpeg", ".png", "webp", ".gif"]:
                    self.preview_peta = self.file_peta
                    super().save(update_fields=["preview_peta"])
                    return

                # jika file adalah pdf
                if ext == ".pdf":

                    pdf_path = self.file_peta.path

                    # buka file pdf
                    doc = fitz.open(pdf_path)

                    page = doc.load_page(0)

                    # Render ke pixmap (bisa di ubah dpi di matrix)
                    zoom = 2
                    mat = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=mat)

                    # simpan ke file
                    image_bytes = pix.tobytes("png")
                    image = Image.open(io.BytesIO(image_bytes))

                    # tentukan path file preview
                    image_path = os.path.join(
                        settings.MEDIA_ROOT,
                        f"data_teknis/peta/{self.jenis_peta.lower()}/previews/",
                        f"{self.pk}_preview.png",
                    )
                    os.makedirs(os.path.dirname(image_path), exist_ok=True)
                    image.save(image_path, "PNG")

                    # simpan path-nya ke model
                    self.preview_peta.name = f"data_teknis/peta/{self.jenis_peta.lower()}/previews/{self.pk}_preview.png"
                    super().save(update_fields=["preview_peta"])

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
    file_foto = models.ImageField(
        "Fot Bendung", upload_to=upload_to_bendung, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Data Bendung"

    def __str__(self):
        return f"Nama Bendung : {self.nama_bendung}"


# data Embung
class EmbungModel(models.Model):
    nama_embung = models.CharField("Nama Embung", max_length=120)
    lokasi = models.CharField("Lokasi", max_length=120)
    file_foto = models.ImageField(
        "Foto (Jika Ada)", upload_to=upload_to_embung, null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Data Embung"

    def __str__(self):
        return f"Nama Embung : {self.nama_embung}"


# data ketesediaan Air
"""
    Note : Data Ketersedian
"""


# ===========> Model Dokumen
class KetersediaanAirModel(models.Model):
    nama_dokumen = models.CharField("Nama Dokumen", max_length=150)
    th = models.CharField("Tahun")
    file_dokumen = models.FileField(
        "PDF File", upload_to=upload_to_ketersediaan_air, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ketersediaan Air"
        verbose_name_plural = "Data Ketersediaan Air"

    def __str__(self):
        return self.nama_dokumen


# ===========> Update Model Baru
# class DASModel(models.Model):
#     nama = models.CharField("Nama DAS", max_length=100)

#     def __str__(self):
#         return self.nama


# class KondisiUtamaModel(models.Model):
#     nama = models.CharField("Nama Kondisi", max_length=100)

#     def __str__(self):
#         return f"{self.pk}-{self.nama}"


# class SubKondisiModel(models.Model):
#     nama = models.CharField("Nama Kondisi", max_length=100)

#     def __str__(self):
#         return self.nama


# class NeracaAirModel(models.Model):
#     das_id = models.ForeignKey(DASModel, on_delete=models.CASCADE, null=True)
#     kondisi_utama_id = models.ForeignKey(
#         KondisiUtamaModel, on_delete=models.CASCADE, null=True
#     )
#     sub_kondisi_id = models.ForeignKey(
#         SubKondisiModel, on_delete=models.CASCADE, null=True, blank=True
#     )
#     parent = models.ForeignKey(
#         "self", on_delete=models.CASCADE, null=True, blank=True, related_name="subitems"
#     )
#     tahun = models.CharField(
#         "Tahun Periode", default="2025-2026", null=True, blank=True
#     )

#     # perubahan data otomatis di simpan ke db
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Neraca Air"
#         verbose_name_plural = "Data Neraca Air"

#     def __str__(self):
#         return f"{self.das_id.nama} - {self.kondisi_utama_id.nama} - {self.sub_kondisi_id.nama if self.sub_kondisi_id else None}"

#     # @property

#     def rata_rata_tahunan(self):
#         print(f"Kondisi ID = {self.sub_kondisi_id}")
#         if self.sub_kondisi_id is not None:
#             return None  # tidak dihitung untuk baris utama
#         nilai_bulanan = self.bulan_values.all()
#         if nilai_bulanan.exists():
#             return round(sum(nb.nilai for nb in nilai_bulanan) / len(nilai_bulanan), 2)
#         return 0

#     # def rata_rata_tahunan(self):
#     #     if not self.sub_kondisi_id:
#     #         return None
#     #     nilai_bulanan = self.bulan_values.all()
#     #     if nilai_bulanan.exists():
#     #         total = sum(nb.nilai for nb in nilai_bulanan)
#     #         return round(total / nilai_bulanan.count(), 2)
#     #     return None

#     def total_subkondisi(self):
#         print(f"Sub Items => {self.subitems}")
#         if not self.subitems.exists():
#             return None
#         total = 0
#         count = 0
#         for sub in self.subitems.all():
#             rata = sub.rata_rata_tahunan()
#             if rata is not None:
#                 total += rata
#                 count += 1
#         return round(total, 3) if count > 0 else None


# class BulanNeracaAirModel(models.Model):
#     PERIODE_CHOICES = [
#         ("I", "Periode I"),
#         ("II", "Periode II"),
#     ]

#     BULAN_CHOICES = [
#         ("Jan", "Januari"),
#         ("Feb", "Februari"),
#         ("Mar", "Maret"),
#         ("Apr", "April"),
#         ("Mei", "Mei"),
#         ("Jun", "Juni"),
#         ("Jul", "Juli"),
#         ("Agu", "Agustus"),
#         ("Sep", "September"),
#         ("Okt", "Oktober"),
#         ("Nov", "November"),
#         ("Des", "Desember"),
#     ]

#     neraca_id = models.ForeignKey(
#         NeracaAirModel, on_delete=models.CASCADE, related_name="bulan_values"
#     )
#     bulan = models.CharField(max_length=4, choices=BULAN_CHOICES)
#     periode = models.CharField(max_length=4, choices=PERIODE_CHOICES)
#     nilai = models.FloatField(default=0)

#     class Meta:
#         unique_together = ("neraca_id", "bulan", "periode")

#     def __str__(self):
#         return f"{self.neraca_id.das_id.nama} - {self.bulan} ({self.periode})"


# ===========> Model Lama
# class KondisiKetersediaanModel(models.Model):
#     nama_kondisi = models.CharField("Nama Kondisi", max_length=150)

#     class Meta:
#         verbose_name_plural = "Master Kondisi Ketersediaan Air"

#     def __str__(self):
#         return f"{self.nama_kondisi}"


# class SubKondisiKetersediaanModel(models.Model):
#     kondisi_ketersediaan_id = models.ForeignKey(
#         KondisiKetersediaanModel, on_delete=models.CASCADE
#     )
#     nama_sub_kondisi = models.CharField("Nama Sub Kondisi", max_length=150)

#     class Meta:
#         verbose_name_plural = "Master Kondisi Ketersediaan Sub"


# class KetersediaanAirModel(models.Model):
#     NAMA_BULAN = (
#         ("", "-- Pilih --"),
#         ("01", "Jan"),
#         ("02", "Feb"),
#         ("03", "Mar"),
#         ("04", "Apr"),
#         ("05", "Mei"),
#         ("06", "Jun"),
#         ("07", "Jul"),
#         ("08", "Agst"),
#         ("09", "Sept"),
#         ("10", "Okt"),
#         ("11", "Nov"),
#         ("12", "Des"),
#     )

#     NAMA_PERIODE = (
#         ("", "-- Pilih --"),
#         ("i", "I"),
#         ("ii", "II"),
#     )
#     nama_das = models.CharField("Nama DAS", max_length=150)
#     kondisi = models.ForeignKey(KondisiKetersediaanModel, on_delete=models.CASCADE)
#     sub_kondisi = ChainedForeignKey(
#         SubKondisiKetersediaanModel,
#         chained_field="kondisi",
#         chained_model_field="kondisi_ketersediaan_id",
#         show_all=False,
#         auto_choose=True,
#         sort=True,
#         on_delete=models.CASCADE,
#     )
#     # sub_kondisi = models.ForeignKey(
#     #     SubKondisiKetersediaanModel, on_delete=models.CASCADE
#     # )
#     bulan = models.CharField("Bulan", choices=NAMA_BULAN)
#     periode = models.CharField("Periode", choices=NAMA_PERIODE)
#     nilai = models.CharField("Nilai", max_length=12, null=True, blank=True)
#     rata_rata_th = models.CharField("Rata-rata Tahunan", max_length=12)
#     ket = models.CharField("Keterangan", max_length=255, null=True, blank=True)

#     class Meta:
#         verbose_name_plural = "Data Ketersediaan Air"

#     def __str__(self):
#         return f"Nama Das {self.nama_das}"


# class NeracaAirModel(models.Model):
#     NAMA_BULAN = (
#         ("", "-- Pilih --"),
#         ("01", "Jan"),
#         ("02", "Feb"),
#         ("03", "Mar"),
#         ("04", "Apr"),
#         ("05", "Mei"),
#         ("06", "Jun"),
#         ("07", "Jul"),
#         ("08", "Agst"),
#         ("09", "Sept"),
#         ("10", "Okt"),
#         ("11", "Nov"),
#         ("12", "Des"),
#     )

#     NAMA_PERIODE = (
#         ("", "-- Pilih --"),
#         ("i", "I"),
#         ("ii", "II"),
#     )

#     SKENARIO = (
#         ("", "-- Pilih --"),
#         ("Kebutuhan Air", "Kebutuhan Air"),
#         ("Kondisi Basah (Debit Air Cukup)", "Kondisi Basah (Debit Air Cukup)"),
#         ("Kondisi Normal (Debit Air Normal)", "Kondisi Normal (Debit Air Normal)"),
#         ("Kondisi Rendah (Debit Air Rendah)", "Kondisi Rendah (Debit Air Rendah)"),
#     )

#     skenario_neraca_air = models.CharField(
#         "Skenario Neraca Air", choices=SKENARIO, max_length=150
#     )
#     bulan = models.CharField("Bulan", choices=NAMA_BULAN)
#     periode = models.CharField("Periode", choices=NAMA_PERIODE)
#     nilai = models.CharField("Nilai", max_length=12, null=True, blank=True)

#     class Meta:
#         verbose_name_plural = "Data Neraca Air"

#     def __str__(self):
#         return f"{self.skenario_neraca_air}"


# NOTE: SKEMA
def upload_to_skema(instance, filename):
    base, ext = os.path.splitext(filename)
    if instance.jenis_skema_id and instance.jenis_skema_id.nama_skema:
        folder_name = instance.jenis_skema_id.nama_skema.lower().replace(" ", "_")
    else:
        folder_name = "lainnya"
    tanggal = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    name_dok = instance.nama_dokumen.lower().replace(" ", "_")
    new_filename = f"{name_dok}_{tanggal}{ext}"

    return os.path.join("data_teknis", "skema", new_filename)


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
        "File Skema (PDF)", upload_to=upload_to_skema, blank=True, null=True
    )
    nama_dokumen = models.CharField("Nama Dokumen", null=True, blank=True)
    th = models.CharField("Tahun Dokumen", blank=True, null=True)
    preview_skema = models.ImageField(
        "Preview", upload_to=upload_to_skema, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        try:
            old = SkemaModel.objects.get(pk=self.pk)
        except SkemaModel.DoesNotExist:
            old = None

        super().save(*args, **kwargs)
        # print(f"Skema File ID => {old.pk}")

        # if self.file_skema and not self.preview_skema:
        if self.file_skema and (not old or old.file_skema != self.file_skema):
            if old and old.file_skema and os.path.isfile(old.preview_skema.path):
                os.remove(old.preview_skema.path)

            ext = os.path.splitext(self.file_skema.name)[1].lower()

            if ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
                self.preview_skema = self.file_skema
                super().save(update_fields=["preview_skema"])

            if ext == ".pdf":
                pdf_path = self.file_skema.path
                # split_name_file = self.file_skema.name.split('.')
                s_name_file = "".join(
                    "".join(
                        "".join(self.file_skema.name.split("/")[-1]).split(".")[0]
                    ).split("_")[-1]
                )

                doc = fitz.open(pdf_path)

                page = doc.load_page(0)

                zoom = 2
                mat = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                # simpan ke file
                image_bytes = pix.tobytes("png")
                image = Image.open(io.BytesIO(image_bytes))

                # tentukan path file preview
                image_path = os.path.join(
                    settings.MEDIA_ROOT,
                    f"data_teknis/skema/",
                    f"{self.pk}_{self.jenis_skema_id.nama_skema}_preview_{s_name_file}.png",
                )
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                rotate = image.rotate(90, expand=True)
                # image.save(image_path, "PNG")
                rotate.save(image_path, "PNG")

                # simpan path nya ke model
                self.preview_skema.name = f"data_teknis/skema/{self.pk}_{self.jenis_skema_id.nama_skema}_preview_{s_name_file}.png"
                super().save(update_fields=["preview_skema"])

    class Meta:
        verbose_name = "Skema"
        verbose_name_plural = "Data Skema"

    def __str__(self):
        return f"{self.jenis_skema_id.nama_skema}"


# NOTE : Jaringan Irigasi Utama
class JenisJaringanModel(models.Model):
    nama_jaringan = models.CharField("Nama Jaringan Irigasi", max_length=100)
    kode = models.CharField("Kode Bangunan", max_length=32, null=True, blank=True)
    panjang = models.DecimalField(
        "Panjang (Km)", null=True, blank=True, max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f"{self.nama_jaringan} {self.kode if self.kode else ''}"


class BangunanModel(models.Model):
    jaringan_id = models.ForeignKey(JenisJaringanModel, on_delete=models.CASCADE)
    kode = models.CharField("Kode Bangunan", max_length=50, null=True, blank=True)
    nama_bangunan = models.CharField("Nama Bangunan", max_length=200)

    class Meta:
        verbose_name = "Bangunan"
        verbose_name_plural = "Data Bangunan"
        ordering = ["nama_bangunan"]

    def __str__(self):
        return f"{self.nama_bangunan} {self.kode}"


class JaringanPrimerModel(models.Model):
    jaringan_id = models.ForeignKey(
        JenisJaringanModel,
        on_delete=models.CASCADE,
        verbose_name="Jenis Jaringan",
        # default="1",
        null=True,
        blank=True,
        related_name="primer",
    )
    # nama_bangunan = models.CharField("Nama Bangunan", max_length=100)
    bangunan_1 = models.ForeignKey(
        BangunanModel,
        on_delete=models.CASCADE,
        related_name="primer_awal",
        null=True,
        blank=True,
    )
    bangunan_2 = models.ForeignKey(
        BangunanModel,
        on_delete=models.CASCADE,
        related_name="primer_akhir",
        null=True,
        blank=True,
    )
    saluran = models.CharField("Saluran/Ruas", max_length=100)
    panjang_saluran = models.DecimalField(
        "Panjang Saluran (M)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    th_pembuatan = models.CharField("Tahun Pembuatan/Rehab", max_length=12)

    class Meta:
        verbose_name_plural = "Data Jaringan Primer"

    def __str__(self):
        return f"{self.saluran}"

    @classmethod
    def total_panjang(cls):
        """Mengihtung total panjang saluran"""
        total = cls.objects.aggregate(total=models.Sum("panjang_saluran"))["total"]
        return total or 0


class JaringanSekunderModel(models.Model):
    jaringan_id = models.ForeignKey(
        JenisJaringanModel,
        on_delete=models.CASCADE,
        verbose_name="Jenis Jaringan",
        blank=True,
        related_name="sekunder",
    )
    bangunan_1 = models.ForeignKey(
        BangunanModel,
        on_delete=models.CASCADE,
        related_name="sekunder_awal",
        null=True,
        blank=True,
    )
    bangunan_2 = models.ForeignKey(
        BangunanModel,
        on_delete=models.CASCADE,
        related_name="sejunder_akhir",
        null=True,
        blank=True,
    )
    saluran = models.CharField("Saluran/Ruas", max_length=100)
    panjang_saluran = models.DecimalField(
        "Panjang Saluran (M)", max_digits=10, decimal_places=2, null=True, blank=True
    )
    th_pembuatan = models.CharField("Tahun Pembuatan/Rehab", max_length=12)

    class Meta:
        verbose_name_plural = "Data Jaringan Sekunder"
        ordering = ["jaringan_id__kode", "saluran", "-th_pembuatan"]

    def __str__(self):
        return f"{self.jaringan_id}"

    @classmethod
    def total_panjang_b_wr_5(cls):
        """Mengihtung total panjang saluran"""
        totalx = cls.objects.filter(jaringan_id__kode="B.WR.5").aggregate(
            total=models.Sum("panjang_saluran")
        )["total"]
        return totalx or 0

    @classmethod
    def total_panjang_b_wr_5_1(cls):
        """Mengihtung total panjang saluran"""
        totalx = cls.objects.filter(jaringan_id__kode="B.WR.5.1").aggregate(
            total=models.Sum("panjang_saluran")
        )["total"]
        return totalx or 0

    @classmethod
    def total_panjang_b_sj(cls):
        """Mengihtung total panjang saluran"""
        totalx = cls.objects.filter(jaringan_id__kode="B.SJ").aggregate(
            total=models.Sum("panjang_saluran")
        )["total"]
        return totalx or 0

    @classmethod
    def total_panjang_b_m(cls):
        """Mengihtung total panjang saluran"""
        totalx = cls.objects.filter(jaringan_id__kode="B.M").aggregate(
            total=models.Sum("panjang_saluran")
        )["total"]
        return totalx or 0

    @classmethod
    def total_panjang_b_or(cls):
        """Mengihtung total panjang saluran"""
        totalx = cls.objects.filter(jaringan_id__kode="B.OR").aggregate(
            total=models.Sum("panjang_saluran")
        )["total"]
        return totalx or 0


class JaringanTersierModel(models.Model):
    jaringan_id = models.ForeignKey(
        JenisJaringanModel,
        on_delete=models.CASCADE,
        verbose_name="Jenis Jaringan",
        blank=True,
        null=True,
        related_name="tersier",
    )
    # nama_bangunan = models.CharField("Nama Bangunan", max_length=100)
    bangunan = models.ForeignKey(
        BangunanModel,
        on_delete=models.CASCADE,
        related_name="tersier",
        null=True,
        blank=True,
    )

    nama_petak = models.CharField(
        "Nama Petak Tersier", max_length=100, default="Petak", help_text="Petak"
    )
    luasan = models.DecimalField(
        "Luasan (HA)", max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = "Jaringan Tersier"
        verbose_name_plural = "Data Jaringan Tersier"

    def __str__(self):
        return f"{self.jaringan_id}"

    @classmethod
    def total_luasan(cls):
        """Mengihtung total luasan"""
        total = cls.objects.aggregate(total=models.Sum("luasan"))["total"]
        return total or 0


# NOTE: Petugas OP
# Jabatan Petugas
# class WilayahKerjaBangunanModel(models.Model)


# class JabatanPetugasOPModel(models.Model):
#     JABATAN_PETUGAS_CHOICE = [
#         ("", "-- Pilih --"),
#         ("Pengamat", "Pengamat"),
#         ("Mantri/Juru", "Mantri/Juru"),
#         ("Petugas Pintu Air (PPA)", "Petugas Pintu Air (PPA)"),
#         ("Petugas Operasi Bendu (POB)", "Petugas Operasi Bendu (POB)"),
#     ]
#     nama_jabatan = models.CharField(
#         "Jabatan", max_length=100, choices=JABATAN_PETUGAS_CHOICE
#     )

#     def __str__(self):
#         return self.nama_jabatan


# # class WilayahKerjaPetugasOPModel(models.Model):
# #     daerah_irigasi_id = models.ForeignKey(
# #         DaerahIrigasiModel,
# #         on_delete=models.CASCADE,
# #         null=True,
# #         blank=True,
# #         verbose_name="Daerah Irigasi",
# #     )
# #     # wilayah_kerja = models.CharField("Wilayah Kerja", max_length=80)
# #     bangunan = models.ForeignKey(
# #         BangunanModel, on_delete=models.SET_NULL, null=True, blank=True
# #     )
# #     luas = models.CharField("Bangunan dan Luas", max_length=50, null=True)

# #     def __str__(self):
# #         return self.bangunan


# class PetugasOPModel(models.Model):
#     # nama_petugas = models.CharField("Nama Petugas", max_length=150)
#     user = models.OneToOneField(
#         UserModel,
#         on_delete=models.CASCADE,
#         related_name="petugas_op",
#         null=True,
#         blank=True,
#     )

#     jabatan_id = models.ForeignKey(
#         JabatanPetugasOPModel,
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         verbose_name="Jabatan",
#     )
#     # wilayah_kerja
#     wilayah_kerja = models.ManyToManyField(
#         BangunanModel,
#         related_name="petugas_op",
#     )
#     luas = models.DecimalField(
#         "Luas (Ha)", max_digits=10, decimal_places=2, null=True, blank=True
#     )

#     class Meta:
#         verbose_name_plural = "Data Petugas OP"

#     def __str__(self):
#         return f"{self.user}"


class JabatanOPModel(models.Model):
    """Jenis jabatan seperti Pengamat, Mantri, PPA, atau POB"""

    JABATAN_PETUGAS_CHOICE = [
        ("", "-- Pilih --"),
        ("Pengamat", "Pengamat"),
        ("Mantri/Juru", "Mantri/Juru"),
        ("Petugas Pintu Air (PPA)", "Petugas Pintu Air (PPA)"),
        ("Petugas Operasi Bendu (POB)", "Petugas Operasi Bendu (POB)"),
    ]

    nama = models.CharField(max_length=100, unique=True, choices=JABATAN_PETUGAS_CHOICE)

    class Meta:
        verbose_name = "Jabatan Petugas OP"
        verbose_name_plural = "Data Jabatan Petugas OP"

    def __str__(self):
        return self.nama


class PetugasOPModel(models.Model):
    """Data utama Petugas Operasi dan Pemeliharaan"""

    user = models.OneToOneField(
        UserModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    jabatan = models.ForeignKey(
        JabatanOPModel, on_delete=models.SET_NULL, null=True, related_name="petugas"
    )
    wilayah_di = models.ForeignKey(
        DaerahIrigasiModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Wilayah D.I.",
    )

    total_luas = models.FloatField(
        blank=True,
        null=True,
        help_text="Total luas wilayah kerja (Ha)",
        verbose_name="Luas (Ha)",
    )

    class Meta:
        verbose_name = "Petugas OP"
        verbose_name_plural = "Data Petugas OP"

    def __str__(self):
        return f"{self.user.nama} - {self.jabatan}"


class BangunanOPModel(models.Model):
    """Daftar bangunan, saluran, bendung, dan jaringan yang ditangani petugas"""

    petugas = models.ForeignKey(
        PetugasOPModel, on_delete=models.CASCADE, related_name="bangunan"
    )
    nama_bangunan = models.CharField("Bangunan", max_length=100, null=True, blank=True)

    luas = models.FloatField(null=True, blank=True, help_text="Luas area (Ha)")
    jenis = models.CharField(
        max_length=50,
        choices=[
            ("primer", "Saluran Primer"),
            ("sekunder", "Saluran Sekunder"),
            ("tersier", "Saluran Tersier"),
            ("bendung", "Bendung"),
            ("lainnya", "Lainnya"),
        ],
        default="lainnya",
    )

    class Meta:
        verbose_name = "Bangunan Wilayah Kerja Petugas OP"
        verbose_name_plural = "Data Wilayah Kerja Petugas OP"

    def __str__(self):
        luas_str = f" ({self.luas} Ha)" if self.luas else ""
        return f"{self.nama_bangunan}{luas_str}"
