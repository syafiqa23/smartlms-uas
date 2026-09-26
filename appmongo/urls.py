from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .api import api
from .views import health, home

urlpatterns = [
    path("health/", health, name="health"),
    path("", home, name="home"), 
    path("", include("appmongo.frontend_urls")),
    path("api/v1/", api.urls),
    path(
        "api/docs",
        RedirectView.as_view(
            pattern_name="smart_lms_api:openapi-view",
            permanent=False,
        ),
        name="api_docs",
    ),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
