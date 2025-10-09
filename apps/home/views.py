from django.shortcuts import render
from apps.masterdata.models import DataUmuModel, SumberAirigasiModel


# Create your views here.
def index_home(request):

    data_sumber_air = SumberAirigasiModel.objects.all()

    data_umum = DataUmuModel.objects.first()
    # print(f"Data Umum : {data_umum.daerah_irigasi_id}")

    context = {
        "page_name": "indexHomePage",
        "dataSumberAir": data_sumber_air,
        "dataUmum": data_umum,
    }
    return render(request, "home/index_home.html", context)
