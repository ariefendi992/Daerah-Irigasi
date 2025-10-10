from django.urls import path
from .views import data_teknis_view

urlpatterns = [path("peta-daerah-irigasi", data_teknis_view, name="petaDI")]
