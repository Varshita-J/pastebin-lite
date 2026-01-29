import os
from datetime import datetime
from django.utils import timezone

def get_now_for_expiry(request):
    if os.environ.get("TEST_MODE") == "1":
        header_value = request.headers.get("x-test-now-ms")
        if header_value:
            try:
                ms = int(header_value)
                return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
            except (ValueError, OSError):
                pass

    return timezone.now()
