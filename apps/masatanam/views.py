from django.shortcuts import render
from .models import *


# Create your views here
def raalisasi_view(request):
    data_realisasi = RealisasiLuasTanamModel.objects.all()
    context = {
        "pageName": "masaTanam",
        "titlePage": "Realisasi lua",
        "heroTitle": "Masa Tanam",
        "heroSubtitle": "#Realisasi Luas Tanam ",
        "realisasi": data_realisasi,
    }

    return render(request, "masatanam/realisasi_luas_tanam_page.html", context)


def produktivitas_view(request):
    data_produktivitas = ProduktivitasPadiModel.objects.all()
    context = {
        "pageName": "masaTanam",
        "titlePage": "Produktivitas Padi",
        "heroTitle": "Masa Tanam",
        "heroSubtitle": "#Produktivitas Padi",
        "produktivitas": data_produktivitas,
    }

    return render(request, "masatanam/produktivitas_page.html", context)
