from re import template
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import View

from .forms import CommentForm, UploadFileForm, LinkSubmissionForm
from .models import Comment, FileSubmission, LinkSubmission


class FileSubmissionView(View):
    form_class = UploadFileForm
    template_name = "upload.html"

    def get(self, request, *args, **kwags):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = FileSubmission(
                title=form.cleaned_data["title"],
                file=request.FILES["file"],
                description=form.cleaned_data["description"],
                private=form.cleaned_data["private"],
                author=request.user,
            )
            instance.save()
            return redirect(
                reverse(
                    "upload:submission",
                    kwargs={"submission_id": instance.id, "submission_type": "file"},
                )
            )
        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class SubmissionView(View):
    form_class = CommentForm
    template_name = "submission.html"

    def get(self, request, *args, **kwargs):
        submission = self.get_submission(
            submission_type=kwargs["submission_type"],
            submission_id=kwargs["submission_id"],
        )
        self.commentList = submission.comments.all().order_by("-created_at")
        form = CommentForm()
        return render(
            request,
            "submission.html",
            {
                "submission": submission,
                "form": form,
                "comments": self.commentList,
                "submission_type": kwargs["submission_type"],
            },
        )

    def post(self, request, *args, **kwargs):
        submission = self.get_submission(
            submission_type=kwargs["submission_type"],
            submission_id=kwargs["submission_id"],
        )
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = Comment(
                comment=request.POST["comment"],
                content_object=submission,
                author=request.user,
            )
            instance.save()
            return redirect(
                reverse(
                    "upload:submission",
                    kwargs={
                        "submission_id": kwargs["submission_id"],
                        "submission_type": kwargs["submission_type"],
                    },
                )
            )

    def get_submission(self, submission_type, submission_id):
        if submission_type == "file":
            submission = get_object_or_404(FileSubmission, pk=submission_id)
        else:
            submission = get_object_or_404(LinkSubmission, pk=submission_id)
        return submission


def submit_view(request):
    if request.user.is_authenticated:
        return render(request, "submission_select.html")
    else:
        return redirect(reverse("main:register"))


class LinkSubmissionView(View):
    form_class = LinkSubmissionForm
    template_name = "submit_link.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = LinkSubmission(
                title=form.cleaned_data["title"],
                link=form.cleaned_data["link"],
                description=form.cleaned_data["description"],
                private=form.cleaned_data["private"],
                author=request.user,
            )
            try:
                instance.full_clean()
                instance.save()
            except ValidationError:
                instance.delete()
                link_error = "Link field is not a valid link. Make sure the link starts with http:// or https://"
                return render(
                    request,
                    self.template_name,
                    {"form": form, "link_error": link_error},
                )
            return redirect(
                reverse(
                    "upload:submission",
                    kwargs={
                        "submission_id": instance.id,
                        "submission_type": "link",
                    },
                )
            )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
