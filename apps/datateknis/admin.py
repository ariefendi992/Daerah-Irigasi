from django.contrib import admin
from django.db.models import Sum
from .models import *

# Register your models here.


# Peta D.I.
@admin.register(PetaDIModel)
class PetaDIAdmin(admin.ModelAdmin):
    list_display = ["jenis_peta", "nama_peta", "deskripsi", "tgl_upload", "file_peta"]
    search_fields = ["nama_peta"]
    list_filter = ["nama_peta", "jenis_peta"]


@admin.register(BendungModel)
class BendungAdmin(admin.ModelAdmin):
    list_display = [
        "nama_bendung",
        "koordinat",
        "lokasi",
        "luas_petak_dialiri",
        "tinggi_bendung",
        "lebar_bendung",
        "th_pembangunan",
    ]
    search_fields = ["nama_bendung"]
    list_filter = ["nama_bendung", "th_pembangunan"]


@admin.register(EmbungModel)
class EmbungAdmin(admin.ModelAdmin):
    list_display = ["nama_embung", "lokasi"]
    search_fields = ["nama_embung", "lokasi"]
    list_filter = ["nama_embung", "lokasi"]


# NOTE : Ketersediaan Air
@admin.register(KondisiKetersediaanModel)
class KondisiKetersediaanAdmin(admin.ModelAdmin):
    # list_display = ["nama_kondisi"]
    def get_model_perms(self, request):
        return {}


@admin.register(SubKondisiKetersediaanModel)
class SubKondisiKetersediaanAdmin(admin.ModelAdmin):
    # list_display = ["nama_sub_kondisi", "kondisi_ketersediaan_id"]
    # list_filter = ["kondisi_ketersediaan_id"]
    def get_model_perms(self, request):
        return {}


@admin.register(KetersediaanAirModel)
class KetersediaanAirAdmin(admin.ModelAdmin):
    list_display = ["nama_das", "kondisi", "sub_kondisi", "bulan", "periode"]
    list_filter = ["kondisi", "bulan", "periode"]


@admin.register(NeracaAirModel)
class NeracaAdmin(admin.ModelAdmin):
    list_display = ["skenario_neraca_air", "bulan", "periode"]
    search_fields = ["skenario_neraca_air", "bulan"]
    list_filter = ["skenario_neraca_air", "bulan"]


# SKEMA
@admin.register(JenisSkemaModel)
class JenisSkemaAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(SkemaModel)
class SkemaAdmin(admin.ModelAdmin):
    list_display = ["jenis_skema_id", "daerah_irigasi_id", "tgl_upload", "file_skema"]
    search_fields = ["jenis_skema_id", "daerah_irigasi_id"]
    list_filter = ["jenis_skema_id"]


# Jaringan Irigasi Utama
@admin.register(JenisJaringanModel)
class JenisJaringanAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(JaringanPrimerModel)
class JaringanPrimerAdmin(admin.ModelAdmin):
    list_display = [
        "jenis_jaringan_id",
        "nama_bangunan",
        "panjang_saluran",
        "th_pembuatan",
    ]
    search_fields = ["jenis_jaringan_id", "nama_bangunan"]
    # list_filter = ["jenis_jaringan_id", "nama_bangunan"]

    def changelist_view(self, request, extra_context=None):
        # Hitung total panjang saluran
        total_panjang = (
            JaringanPrimerModel.objects.aggregate(Sum("panjang_saluran"))[
                "panjang_saluran__sum"
            ]
            or 0
        )

        extra_context = extra_context or {}
        extra_context["total_panjang"] = total_panjang
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(JaringanSekunderModel)
class JaringanSekunderAdmin(admin.ModelAdmin):
    list_display = [
        "jenis_jaringan_id",
        "nama_bangunan",
        "panjang_saluran",
        "th_pembuatan",
    ]
    search_fields = ["jenis_jaringan_id", "nama_bangunan"]
    list_filter = ["jenis_jaringan_id", "nama_bangunan"]

    def changelist_view(self, request, extra_context=None):
        # Hitung total panjang saluran
        total_panjang = (
            JaringanPrimerModel.objects.aggregate(Sum("panjang_saluran"))[
                "panjang_saluran__sum"
            ]
            or 0
        )

        extra_context = extra_context or {}
        extra_context["total_panjang"] = total_panjang
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(JaringanTersierModel)
class JaringanTersierAdmin(admin.ModelAdmin):
    list_display = ["jenis_jaringan_id", "nama_bangunan", "nama_petak", "luasan"]

    def changelist_view(self, request, extra_context=None):
        # Hitung total luasan semua data
        total_luasan = (
            JaringanTersierModel.objects.aggregate(Sum("luasan"))["luasan__sum"] or 0
        )
        extra_context = extra_context or {}
        extra_context["total_luasan"] = total_luasan
        return super().changelist_view(request, extra_context=extra_context)


# NOTE: Petugas OP
@admin.register(JabatanPetugasOPModel)
class JabatanPetugasOPAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(WilayahKerjaPetugasOPModel)
class WilayahKerjaPetugasOPAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(PetugasOPModel)
class PetugasOPAdmin(admin.ModelAdmin):
    list_display = ["nama_petugas", "jabatan_id", "get_wilayah_kerja"]
    filter_horizontal = ("wilayah_kerja",)
    # search_fields = ["nama_petugas", "jabatan_id"]

    def get_wilayah_kerja(self, obj):
        return ", ".join([w.wilayah_kerja for w in obj.wilayah_kerja.all()])

    get_wilayah_kerja.short_description = "Wilayah Kerja"
