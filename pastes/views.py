from datetime import timedelta

from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from rest_framework.exceptions import NotFound

from .models import Paste
from .utils import get_now_for_expiry

def paste_html_view(request, id):
    paste = get_object_or_404(Paste, id=id, is_active=True)

    if not paste.is_active:
        raise NotFound("This paste is no longer available.")

    now = get_now_for_expiry(request)

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


    return render(
        request,
        "paste_view.html",
        {"content": paste.content},
        status=200,
    )

def home_view(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        ttl = request.POST.get("ttl_seconds")
        max_views = request.POST.get("max_views")

        if not content:
            return render(request, "home.html", {"error": "Content is required"})


        expires_at = None
        if ttl:
            expires_at = timezone.now() + timedelta(seconds=int(ttl))

        paste = Paste.objects.create(
            content=content,
            max_views=max_views or None,
            expires_at=expires_at,
        )

        return redirect(f"/p/{paste.id}")

    return render(request, "home.html")
