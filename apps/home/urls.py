from django.urls import path
from .views import index_home

urlpatterns = [path("", index_home, name="homePage")]
