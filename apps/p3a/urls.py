from django.urls import path
from .views import *

urlpatterns = [
    path("daftar-p3a/", daftar_p3a_view, name="daftarP3A"),
]
 