from django.urls import path
from .views import *

urlpatterns = [
    path("peta-daerah-irigasi", data_teknis_view, name="petaDI"),
    path(
        "peta-daerah-irigasi/detail-peta/<int:peta_id>/",
        detail_peta_view,
        name="detailPetaDI",
    ),
    path("sumber-air-irigasi/bendung/", bendung_view, name="bendung"),
    path(
        "sumber-air-irigasi/bendung/<int:bendung_id>/",
        detail_bendung_view,
        name="detailBendung",
    ),
    path("sumber-air-irigasi/embung/", embung_view, name="embung"),
    path(
        "sumber-air-irigasi/",
        sumber_air_view,
        name="sumberAir",
    ),
    path(
        "skema/",
        skema_view,
        name="skema",
    ),
    path("jaringan-irigasi-utama/primer", jaringan_primer_view, name="jaringanPrimer"),
    path(
        "jaringan-irigasi-utama/sekunder",
        jaringan_sekunder_view,
        name="jaringanSekunder",
    ),
    path(
        "jaringan-irigasi-utama/tersier",
        jaringan_tersier_view,
        name="jaringanTersier",
    ),
    path(
        "petugas-op",
        petugas_op_view,
        name="petugasOP",
    ),
    path(
        "petugas-op/<int:petugas_id>/",
        detail_petugas_op_view,
        name="petugasOPDetail",
    ),
]
