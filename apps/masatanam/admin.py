from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(ProduktivitasPadiModel)
class ProduktivitasPadiAdmin(admin.ModelAdmin):
    list_display = [
        "th",
        "tingkat_data",
        "produktivitas_daerah",
        "produktivitas_rata_nasional",
        "presentase",
        "sumber_data",
    ]

    list_filter = ("tingkat_data", "th")
    search_fields = ("sumber_data", "link_sumber")
    readonly_fields = ["presentase"]
    ordering = ("-th",)

    fieldsets = (
        (
            "Informasi Data",
            {
                "fields": (
                    "th",
                    "tingkat_data",
                    "sumber_data",
                    "link_sumber",
                )
            },
        ),
        (
            "Nilai Produktivitas",
            {
                "fields": (
                    "produktivitas_rata_nasional",
                    "produktivitas_daerah",
                    "presentase",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Hitung otomatis presentase sebelum disimpan"""
        if obj.produktivitas_rata_nasional > 0:
            hasil = (obj.produktivitas_daerah / obj.produktivitas_rata_nasional) * 100
            obj.presentase = min(hasil, 100)  # Maksimum 100%

        super().save_model(request, obj, form, change)


# NOTE REALISASI LUAS TANAM
@admin.register(RealisasiLuasTanamModel)
class RealisasiLuasTanamAdmin(admin.ModelAdmin):
    list_display = [
        "th",
        "luas_potensial",
        "mt1",
        "mt2",
        "mt3",
        "area_tanam",
        "ip_ada",
        "persen_realisasi",
        "sumber_data",
    ]
    list_filter = ["th"]
    readonly_fields = ["area_tanam", "ip_ada", "persen_realisasi"]
    ordering = ["-th"]
    search_fields = ["sumber_data", "link_sumber", "th"]

    fieldsets = (
        ("Informasi data", {"fields": ("th", "sumber_data", "link_sumber")}),
        (
            "Data Luas Tanam (Ha)",
            {"fields": ("luas_potensial", "mt1", "mt2", "mt3", "area_tanam")},
        ),
        ("Indeks Pertanaman", {"fields": ("ip_maks", "ip_ada", "persen_realisasi")}),
    )

    def save_model(self, request, obj, form, change):
        """Hitung otomatis sebelum disimpan di admin"""
        obj.area_tanam = (obj.mt1 or 0) + (obj.mt2 or 0) + (obj.mt3 or 0)

        if obj.luas_potensial > 0:
            obj.ip_ada = (obj.area_tanam / obj.luas_potensial) * 100
            obj.persen_realisasi = (
                (obj.ip_ada / obj.ip_maks) * 100 if obj.ip_maks > 0 else 0
            )
        super().save_model(request, obj, form, change)
