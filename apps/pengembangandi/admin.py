from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(JenisPetaPengembanganDIModel)
class JenisPetaPengembanganAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(PengembanganDaerahIrigasiModel)
class PengembanganDaerahIrigasiAdmin(admin.ModelAdmin):
    list_display = [
        "daerah_irigasi_id",
        "jenis_peta_id",
        "sumber_data",
        "keterangan",
        "tgl_upload",
        "file_peta",
    ]

    fieldsets = (
        (
            "Informasi Daerah Irigasi",
            {
                "fields": (
                    "daerah_irigasi_id",
                    "jenis_peta_id",
                    "sumber_data",
                    "keterangan",
                )
            },
        ),
        (
            "Unggah Peta Pengembangan",
            {
                "fields": ("file_peta",),
            },
        ),
    )
