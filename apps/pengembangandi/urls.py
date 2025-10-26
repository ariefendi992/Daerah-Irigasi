from django.urls import path
from .views import *

urlpatterns = [
    path("peta-pengembangan/", peta_pengembangan_view, name="petaPengembanganPage")
]
