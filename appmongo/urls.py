from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from .api import api
from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("", include("appmongo.frontend_urls")),
    path("api/v1/", api.urls),
    path("api/docs", RedirectView.as_view(url="/api/v1/docs", permanent=False)),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
