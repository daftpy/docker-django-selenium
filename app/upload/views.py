from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.views import View

from .forms import CommentForm, UploadFileForm, LinkSubmissionForm
from .models import Comment, FileSubmission, LinkSubmission


class FileSubmissionView(View):
    form_class = UploadFileForm
    template_name = 'upload.html'

    def get(self, request, *args, **kwags):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = FileSubmission(
                    title=form.cleaned_data['title'],
                    file=request.FILES['file'],
                    description=form.cleaned_data['description'],
                    private=form.cleaned_data['private'],
                    author=request.user
                )
            instance.save()
            return redirect(
                reverse(
                    'upload:submission',
                    kwargs={
                        'submission_id': instance.id,
                        'submission_type': 'file'
                    }
                )
            )
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

def submission(request, submission_id, submission_type):
    if submission_type == 'file':
        submission = get_object_or_404(FileSubmission, pk=submission_id)
    else:
        submission = get_object_or_404(LinkSubmission, pk=submission_id)
    commentList = submission.comments.all().order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = Comment(
                comment=request.POST['comment'],
                content_object=submission,
                author=request.user
            )
            instance.save()
            return redirect(reverse(
                'upload:submission', kwargs={'submission_id': submission_id, 'submission_type': submission_type}
            ))
    form = CommentForm()
    return render(request, 'submission.html', {
        'submission': submission,
        'form': form,
        'comments': commentList,
        'submission_type': submission_type
    })

def submit_view(request):
    if request.user.is_authenticated:
        return render(request, 'submission_select.html')
    else:
        return redirect(reverse('main:register'))

def submit_link(request):
    if request.user.is_authenticated:
        form = LinkSubmissionForm()
        if request.method == 'POST':
            form = LinkSubmissionForm(request.POST)
            if form.is_valid():
                instance = LinkSubmission(
                    title=request.POST['title'],
                    link=request.POST['link'],
                    description=request.POST['description'],
                    private=form.cleaned_data['private'],
                    author=request.user
                )
                instance.save()
                return redirect(reverse(
                    'upload:submission', kwargs={
                        'submission_id': instance.id,
                        'submission_type': 'link'
                    }
                ))
        return render(request, 'submit_link.html', {'form': form})
    else:
        return redirect(reverse('main:register'))
