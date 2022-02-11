import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Submission(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=256)
    file = models.FileField()
    private = models.BooleanField(default=False)


class Comment(models.Model):
    # Upgrade with generic relations so we can associate comments with either
    # FileSubmissions or LinkSubmissions
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255)

# Build out link submission model

# Build out reaction model
    