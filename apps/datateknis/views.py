from django.shortcuts import render


# Create your views here.
def data_teknis_view(request):

    context = {"pageName": "dataTeknis"}
    return render(request, "datateknis/peta_page.html", context)
