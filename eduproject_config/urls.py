from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app_base.urls")),

    path('user/', include('allauth.urls')),
    path("user/", include("app_accounts.urls")),
    path("exercises/", include("app_exercises.urls")),
    path("dashboard/", include("app_dashboard.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
