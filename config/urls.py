from django.contrib import admin
from django.urls import path, include

from config.schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("agency.urls")),
]
urlpatterns += swagger_urlpatterns
