from django.contrib import admin
from .models import Comment, FileSubmission

# Register your models here.
admin.site.register(FileSubmission)
admin.site.register(Comment)
