from django.urls import path
from .views import *

urlpatterns = [path("monitoring/", index_monitoring, name="indexMonitoringPage")]
