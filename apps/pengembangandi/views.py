from django.shortcuts import render
from .models import *


# Create your views here.
def peta_pengembangan_view(request):

    data_peta = PengembanganDaerahIrigasiModel.objects.all()

    context = {
        "pageName": "pengembangan",
        "titlePage": "Peta pengembangan",
        "heroTitle": "Pengembangan Dareah Irigasi",
        "heroSubtitle": "#Peta Pengembangan",
        "dataPeta": data_peta,
    }
    return render(request, "pengembangan/peta_pengembangan_page.html", context)
