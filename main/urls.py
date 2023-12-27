"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from transpose.views import upload_audio, CheckPidExistViewSet
from rest_framework.routers import DefaultRouter
from index.views import index_view
from umx import views as umx_view
from event_handler.views import EventHandlerViewSet
from runconvert.views import RunConvertViewSet
from midi2sheet.views import MidiToSheetViewSet
from library_render.views import library_render_generate

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("index.html", index_view, name="index_view"),
    path("_api/transpose/upload_file", upload_audio, name="upload_audio"),
    path("_api/library_render", library_render_generate),
    path("_api/transpose/check_pid_working", CheckPidExistViewSet.as_view({"post":"update"}), name="CheckPidExist"),
    path("_api/model/umx/start/", umx_view.UMXViewSet.as_view({"post":"create"})),
    path("_api/model/runconvert/start/", RunConvertViewSet.as_view({"post":"create"})),
    path("_api/model/event_handler/get_progress", EventHandlerViewSet.as_view({"post":"get_progress"})),
    path("_api/model/event_handler/create", EventHandlerViewSet.as_view({"post":"create"})),
    path("_api/model/event_handler/update", EventHandlerViewSet.as_view({"post":"partial_update"})),
    path("_api/model/midi2sheet", MidiToSheetViewSet.as_view({"post":"create"})),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)