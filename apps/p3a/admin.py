from django.contrib import admin
from .models import *


# Register your models here.
class PetakTersierInline(admin.TabularInline):
    model = PetakTersierModel
    extra = 1
    fields = ("nama_petak", "nomenklatur", "luas")
    show_change_link = True


@admin.register(P3AModel)
class P3AAdmin(admin.ModelAdmin):
    list_display = [
        "nama_p3a",
        "desa",
        "kecamatan",
        "kabupaten",
        "luas_area_fungsional",
        "total_luas_petak",
        "sk_bupati",
        "akta_notaris",
    ]

    # filter_horizontal = ("petak_tersier",)
    inlines = [PetakTersierInline]
    search_fields = ["nama_p3a", "desa"]
    list_filter = ["kabupaten", "kecamatan"]


# @admin.register(PetakTersierModel)
# class PetakTersierAdmin(admin.ModelAdmin):
#     list_display = ["nama_petak", "nomenklatur", "luas"]
