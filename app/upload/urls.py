from django.urls import path
from . import views

app_name = "upload"
urlpatterns = [
    # ex: /polls/
    path("", views.submit_view, name="submit_select"),
    path("file/", views.FileSubmissionView.as_view(), name="submit_file"),
    path("link/", views.LinkSubmissionView.as_view(), name="submit_link"),
    path(
        "<str:submission_type>/<str:submission_id>/",
        views.SubmissionView.as_view(),
        name="submission",
    ),
    # path("test/", views.LinkSubmissionView.as_view(), name="test"),
]
