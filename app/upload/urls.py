from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
    # ex: /polls/
    path('', views.image_upload, name='index'),
    path(
        'submission/<str:submission_id>/', views.submission, name='submission'
    )
]