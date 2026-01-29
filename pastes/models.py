from django.db import models
from shortuuidfield import ShortUUIDField
from django.core.validators import MinValueValidator

class Paste(models.Model):
    id = ShortUUIDField(
        unique=True,
        primary_key=True,
        max_length=20,
    )
    content = models.TextField()
    max_views = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(db_index=True, null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
