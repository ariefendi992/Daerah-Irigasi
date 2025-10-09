from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(DaerahIrigasiModel)
class DaerahIrigasiAdmin(admin.ModelAdmin):
    list_display = ["nama_irigasi", "lokasi"]
    search_fields = ["nama_irigasi"]
    list_filter = ["nama_irigasi"]


@admin.register(SumberAirigasiModel)
class SumberAirIrigasiAdmin(admin.ModelAdmin):
    list_display = ["nama_sumber_air", "selengkap_url"]


# NOTE: DATA UMUM
@admin.register(DataUmuModel)
class DataUmumAdmin(admin.ModelAdmin):
    list_display = ["daerah_irigasi_id", "created_at", "deskripsi"]


# @admin.register(TipeSaluranModel)
# class TipeSaluranAdmin(admin.ModelAdmin):
#     list_display = ["nama_tipe"]
#     search_fields = ["nama_tipe"]
#     list_filter = ["nama_tipe"]


# @admin.register(KondisiSaluranModel)
# class KondisiSaluranAdmin(admin.ModelAdmin):
#     list_display = ["nama_kondisi"]
#     search_fields = ["nama_kondisi"]
#     list_filter = ["nama_kondisi"]


# @admin.register(JenisBangunanModel)
# class JenisBangunanAdmin(admin.ModelAdmin):
#     list_display = ["nama_jenis"]
#     search_fields = ["nama_jenis"]
#     list_filter = ["nama_jenis"]


# @admin.register(SaluranModel)
# class SaluranAdmin(admin.ModelAdmin):
#     list_display = [
#         "nama_saluran",
#         "tipe_id",
#         "panjang_saluran",
#         "kondisi_id",
#         "koordinat_start",
#         "koordinat_end",
#     ]

#     search_fields = ["nama_saluran"]
#     list_filter = ["nama_saluran"]


# @admin.register(BangunanModel)
# class BangunanAdmin(admin.ModelAdmin):
#     list_display = ["saluran_id", "nama_bangunan", "jenis_id", "kondisi", "koordinat"]
#     search_fields = ["nama_bangunan"]
#     list_filter = ["nama_bangunan"]


# @admin.register(PetakModel)
# class PetakAdmin(admin.ModelAdmin):
#     list_display = ["saluran_id", "luas", "desa", "kelompok_tani"]
#     search_fields = ["kelompok_tani", "saluran_id", "desa"]
#     list_filter = ["kelompok_tani", "saluran_id", "desa"]
