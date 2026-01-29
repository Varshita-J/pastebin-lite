from .models import Paste
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

class PasteCreateSerializer(serializers.ModelSerializer):
    ttl_seconds = serializers.IntegerField(
        required=False,
        min_value=1,
        write_only=True
    )

    class Meta:
        model = Paste
        fields = ("content", "max_views", "ttl_seconds")

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content must be a non-empty string.")
        return value

    def create(self, validated_data):
        ttl_seconds = validated_data.pop("ttl_seconds", None)

        expires_at = None
        if ttl_seconds:
            expires_at = timezone.now() + timedelta(seconds=ttl_seconds)

        paste = Paste.objects.create(
            expires_at=expires_at,
            **validated_data
        )
        return paste

class PasteRetrieveSerializer(serializers.ModelSerializer):
    remaining_views = serializers.SerializerMethodField()

    class Meta:
        model = Paste
        fields = ("content", "remaining_views", "expires_at")

    def get_remaining_views(self, obj):
        if obj.max_views is None:
            return None
        return max(obj.max_views - obj.view_count, 0)