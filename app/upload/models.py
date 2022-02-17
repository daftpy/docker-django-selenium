import uuid
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class Comment(models.Model):
    # Upgrade with generic relations so we can associate comments with either
    # FileSubmissions or LinkSubmissions
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey("content_type", "object_id")
    object_id = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255)


class FileSubmission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=256)
    file = models.FileField()
    private = models.BooleanField(default=False)
    comments = GenericRelation(Comment)


class LinkSubmission(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=256)
    link = models.CharField(max_length=256)
    private = models.BooleanField(default=False)
    comments = GenericRelation(Comment)

    def clean(self):
        validate = URLValidator()
        try:
            validate(self.link)
        except ValidationError as e:
            raise ValidationError({"link": e})


# Build out reaction model
