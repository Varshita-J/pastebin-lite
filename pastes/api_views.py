from django.db import connection
from django.db.models import F
from django.http import JsonResponse

from rest_framework import generics, status
from rest_framework.response import Response

from . import serializers as api_serializers
from .models import Paste
from .utils import get_now_for_expiry

def healthz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"ok": True}, status=200)
    except Exception:
        return JsonResponse({"ok": False}, status=500)

class PasteCreateAPIView(generics.CreateAPIView):
    queryset = Paste.objects.all()
    serializer_class = api_serializers.PasteCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        paste = serializer.save()

        return Response(
            {
                "id": paste.id,
                "url": f"https://your-app.vercel.app/p/{paste.id}",
            },
            status=status.HTTP_201_CREATED,
        )

class PasteRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Paste.objects.filter(is_active=True)
    serializer_class = api_serializers.PasteRetrieveSerializer
    lookup_field = "id"

    def get_object(self):
        paste = super().get_object()

        if not paste.is_active:
            raise NotFound("This paste is no longer available.")

        now = get_now_for_expiry(self.request)

        if paste.expires_at and paste.expires_at <= now:
            paste.is_active = False
            paste.save(update_fields=["is_active"])
            raise NotFound("This paste has expired.")

        paste.view_count = F("view_count") + 1
        paste.save(update_fields=["view_count"])
        paste.refresh_from_db()
        
        if paste.max_views and paste.view_count >= paste.max_views:
            paste.is_active = False
            paste.save(update_fields=["is_active"])

        return paste

