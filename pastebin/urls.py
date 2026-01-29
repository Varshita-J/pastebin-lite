from django.contrib import admin
from django.urls import path, include
from pastes import views as html_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # API routes
    path("api/", include("pastes.urls")),

    # HTML routes
    path("", html_views.home_view, name="home"),
    path("p/<str:id>/", html_views.paste_html_view, name="paste-view"),
]
