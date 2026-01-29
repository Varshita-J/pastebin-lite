from django.urls import path
from . import api_views

urlpatterns = [
    path("healthz", api_views.healthz, name="healthz"),
    path("pastes", api_views.PasteCreateAPIView.as_view(), name="create-paste"),
    path("pastes/<str:id>", api_views.PasteRetrieveAPIView.as_view(), name="fetch-paste")
]
