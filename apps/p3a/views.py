from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator


# Create your views here.
def daftar_p3a_view(request):

    data_p3a = P3AModel.objects.all()
    paginator = Paginator(data_p3a, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "pageName": "p3a",
        "titlePage": "P3A",
        "heroTitle": "P3A",
        "heroSubtitle": "#Daftar & Wilayah Kerja P3A",
        "dataP3A": data_p3a,
        "page_obj": page_obj,
    }
    return render(request, "p3a/daftar_p3a_page.html", context)
