from django.shortcuts import render


# Create your views here.
def index_monitoring(request):

    context = {"page_name": "indexMonitoringPage"}
    return render(request, "monitoring/index_monitoring.html", context)
