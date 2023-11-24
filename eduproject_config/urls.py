from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_base.urls")),

    path('user/', include('allauth.urls')),
    path("user/", include("app_accounts.urls")),
]

