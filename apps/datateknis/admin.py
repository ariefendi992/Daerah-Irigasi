from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import *

# Register your models here.


# Peta D.I.
@admin.register(PetaDIModel)
class PetaDIAdmin(admin.ModelAdmin):
    list_display = [
        "jenis_peta",
        "nama_peta",
        "deskripsi",
        "tgl_upload",
        "file_peta",
        "preview_tag",
    ]
    search_fields = ["nama_peta"]
    list_filter = ["nama_peta", "jenis_peta"]
    fieldsets = [("", {"fields": ["jenis_peta", "deskripsi", "file_peta"]})]

    def preview_tag(self, obj):
        if obj.preview_peta:
            return format_html(
                '<div style="display: flex; flex-direction: column; align-items: center;">'
                '<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; margin-bottom: 5px; border-radius: 4px;" />'
                "</div>",
                obj.preview_peta.url,
            )

        return "belum ada preview"

    preview_tag.short_description = "Preview"


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
# ======================> Dokumen Only
@admin.register(KetersediaanAirModel)
class KetersediaanAirAdmin(admin.ModelAdmin):
    list_display = ["nama_dokumen", "th", "file_dokumen"]
    search_fields = ["nama_dokumen", "th"]


# ======================> Kode Baru
# class BulanNeracaInline(admin.TabularInline):
#     model = BulanNeracaAirModel
#     extra = 0
#     # fields = ["bulan", "periode", "nilai"]
#     # ordering = ["bulan", "periode"]


# @admin.register(DASModel)
# class DASAdmin(admin.ModelAdmin):

#     def get_model_perms(self, request):
#         return {}


# @admin.register(KondisiUtamaModel)
# class KondisiUtamaAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}


# @admin.register(SubKondisiModel)
# class SubKondisiAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}


# @admin.register(NeracaAirModel)
# class NeracaAirAdmin(admin.ModelAdmin):
#     list_display = [
#         "das_id",
#         "kondisi_utama_id",
#         "sub_kondisi_id",
#         "tahun",
#         "rata_rata_display",
#         "total_sub_display",
#     ]
#     list_filter = ["das_id", "kondisi_utama_id", "sub_kondisi_id", "tahun"]
#     search_fields = ["das_id__nama", "sub_kondi_id__nama"]
#     inlines = [BulanNeracaInline]

#     def rata_rata_display(self, obj):
#         return obj.rata_rata_tahunan() or "—"

#     rata_rata_display.short_description = "Rata-rata Tahunan"

#     def total_sub_display(self, obj):
#         return obj.total_subkondisi() or "—"

#     total_sub_display.short_description = "Total dari Sub Kondisi"


# ======================> Kode Lama
# @admin.register(KondisiKetersediaanModel)
# class KondisiKetersediaanAdmin(admin.ModelAdmin):
#     # list_display = ["nama_kondisi"]
#     def get_model_perms(self, request):
#         return {}


# @admin.register(SubKondisiKetersediaanModel)
# class SubKondisiKetersediaanAdmin(admin.ModelAdmin):
#     # list_display = ["nama_sub_kondisi", "kondisi_ketersediaan_id"]
#     # list_filter = ["kondisi_ketersediaan_id"]
#     def get_model_perms(self, request):
#         return {}


# @admin.register(KetersediaanAirModel)
# class KetersediaanAirAdmin(admin.ModelAdmin):
#     list_display = ["nama_das", "kondisi", "sub_kondisi", "bulan", "periode"]
#     list_filter = ["kondisi", "bulan", "periode"]


# @admin.register(NeracaAirModel)
# class NeracaAdmin(admin.ModelAdmin):
#     list_display = ["skenario_neraca_air", "bulan", "periode"]
#     search_fields = ["skenario_neraca_air", "bulan"]
#     list_filter = ["skenario_neraca_air", "bulan"]


# SKEMA
@admin.register(JenisSkemaModel)
class JenisSkemaAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(SkemaModel)
class SkemaAdmin(admin.ModelAdmin):
    list_display = ["jenis_skema_id", "daerah_irigasi_id", "created_at", "file_skema"]
    fieldsets = [
        (
            "",
            {
                "fields": [
                    "jenis_skema_id",
                    "daerah_irigasi_id",
                    "nama_dokumen",
                    "th",
                    "file_skema",
                ]
            },
        )
    ]
    search_fields = ["jenis_skema_id", "daerah_irigasi_id"]
    list_filter = ["jenis_skema_id"]


# Jaringan Irigasi Utama
@admin.register(JenisJaringanModel)
class JenisJaringanAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(BangunanModel)
class BangunanAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(JaringanPrimerModel)
class JaringanPrimerAdmin(admin.ModelAdmin):
    list_display = [
        "jaringan_id",
        "panjang_saluran",
        "th_pembuatan",
    ]
    search_fields = [
        "jaringan_id",
    ]
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
        "jaringan_id",
        "bangunan",
        "saluran",
        "panjang_saluran",
        "th_pembuatan",
    ]
    search_fields = ["jaringan_id", "bangunan"]
    list_filter = ["jaringan_id", "th_pembuatan"]

    def bangunan(self, obj):
        bangunan_1 = f"{obj.bangunan_1}"
        bangunan_2 = f"{obj.bangunan_2} "
        return f"{bangunan_1} - {bangunan_2}"

    def changelist_view(self, request, extra_context=None):
        # Hitung total panjang saluran
        extra_context = extra_context or {}
        # total_panjangx = (
        #     JaringanSekunderModel.objects.aggregate(Sum("panjang_saluran"))[
        #         "panjang_saluran__sum"
        #     ]
        #     or 0
        # )
        total_panjang_bwr_5 = (
            JaringanSekunderModel.objects.filter(jaringan_id__kode="B.WR.5").aggregate(
                Sum("panjang_saluran")
            )["panjang_saluran__sum"]
            or 0
        )
        total_panjang_bwr_5_1 = (
            JaringanSekunderModel.objects.filter(
                jaringan_id__kode="B.WR.5.1"
            ).aggregate(Sum("panjang_saluran"))["panjang_saluran__sum"]
            or 0
        )
        total_panjang_bsj = (
            JaringanSekunderModel.objects.filter(jaringan_id__kode="B.SJ").aggregate(
                Sum("panjang_saluran")
            )["panjang_saluran__sum"]
            or 0
        )
        total_panjang_bm = (
            JaringanSekunderModel.objects.filter(jaringan_id__kode="B.M").aggregate(
                Sum("panjang_saluran")
            )["panjang_saluran__sum"]
            or 0
        )
        total_panjang_bor = (
            JaringanSekunderModel.objects.filter(jaringan_id__kode="B.OR").aggregate(
                Sum("panjang_saluran")
            )["panjang_saluran__sum"]
            or 0
        )

        extra_context["total_bwr_5"] = total_panjang_bwr_5
        extra_context["total_bwr_5_1"] = total_panjang_bwr_5_1
        extra_context["total_bsj"] = total_panjang_bsj
        extra_context["total_bm"] = total_panjang_bm
        extra_context["total_bor"] = total_panjang_bor
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(JaringanTersierModel)
class JaringanTersierAdmin(admin.ModelAdmin):
    list_display = ["jaringan_id", "bangunan", "petak", "luasan"]

    def petak(self, obj):
        return f"{obj.nama_petak} {obj.bangunan.kode}"

    def changelist_view(self, request, extra_context=None):
        # Hitung total luasan semua data
        total_luasan = (
            JaringanTersierModel.objects.aggregate(Sum("luasan"))["luasan__sum"] or 0
        )
        extra_context = extra_context or {}
        extra_context["total_luasan"] = total_luasan
        return super().changelist_view(request, extra_context=extra_context)


# NOTE: Petugas OP <=============
# @admin.register(JabatanPetugasOPModel)
# class JabatanPetugasOPAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         return {}


# # @admin.register(WilayahKerjaPetugasOPModel)
# # class WilayahKerjaPetugasOPAdmin(admin.ModelAdmin):
# #     def get_model_perms(self, request):
# #         return {}


# class PetugasBangunanInline(admin.TabularInline):
#     model = BangunanModel
#     # extra = 1
#     # autocomplete_fields = ["bangunan"]


# @admin.register(PetugasOPModel)
# class PetugasOPAdmin(admin.ModelAdmin):
#     list_display = ["user", "jabatan_id", "get_wilayah_kerja", "luas"]
#     # inlines = [PetugasBangunanInline]

#     filter_horizontal = ["wilayah_kerja"]
#     # search_fields = ["nama_petugas", "jabatan_id"]

#     def get_wilayah_kerja(self, obj):
#         # ambil semua nama wilayah dari relasi ManyToMany
#         return ", ".join([w.nama_bangunan for w in obj.wilayah_kerja.all()])
#         # print(f"Object => {obj}")
#         # return ""


#     get_wilayah_kerja.short_description = "Wilayah Kerja"
class BangunanInline(admin.TabularInline):
    model = BangunanOPModel
    extra = 1


@admin.register(PetugasOPModel)
class PetugasOPAdmin(admin.ModelAdmin):
    list_display = (
        "user__nama",
        "jabatan",
        "wilayah_di",
        "total_luas",
        "get_bangunan",
    )
    search_fields = ("nama_petugas", "jabatan__nama", "wilayah_di")
    list_filter = ("jabatan",)
    inlines = [BangunanInline]

    # def get_bangunan(self, obj):
    #     return ", ".join(
    #         [
    #             b.nama_bangunan.nama_bangunan
    #             for b in obj.bangunan.all()
    #             if b.nama_bangunan
    #         ]
    #     )
    def get_bangunan(self, obj):
        return ", ".join([b.nama_bangunan for b in obj.bangunan.all()])

    get_bangunan.short_description = "Wilayah Kerja"


@admin.register(JabatanOPModel)
class JabatanOPAdmin(admin.ModelAdmin):
    list_display = ("nama",)
    search_fields = ("nama",)


@admin.register(BangunanOPModel)
class BangunanOPAdmin(admin.ModelAdmin):
    list_display = ("nama_bangunan", "petugas", "jenis", "luas")
    list_filter = ("jenis",)
    search_fields = ("nama_bangunan", "petugas__nama_petugas")
