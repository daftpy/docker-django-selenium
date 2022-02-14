from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
    # ex: /polls/
    path('', views.submit_view, name='submit_select' ),
    path('file/', views.image_upload, name='submit_file'),
    path('link/', views.submit_link, name='submit_link'),
    path(
        '<str:submission_type>/<str:submission_id>/', views.submission, name='submission'
    )
]