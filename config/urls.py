"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .settings import *
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chaining/", include("smart_selects.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", include("apps.home.urls"), name="homePage"),
    path("", include("apps.monitoring.urls"), name="monitoringPage"),
    path("data-tenik/", include("apps.datateknis.urls"), name="dataTeknisPage"),
    path("p3a/", include("apps.p3a.urls"), name="dataP3APage"),
]


# admin site
admin.site.site_header = "Daerah Irigasi Papua Barat"
admin.site.site_title = "Administrator"
admin.site.index_title = "Selamat Datang di Dashboard"

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
