from django.urls import path
from .views import *

urlpatterns = [
    path("realisasi-masa-tanam/", raalisasi_view, name="realisasiPage"),
    path("produktivitas-padai/", produktivitas_view, name="produktivitasPage"),
]
