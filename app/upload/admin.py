from django.contrib import admin
from .models import Comment, Submission

# Register your models here.
admin.site.register(Submission)
admin.site.register(Comment)
