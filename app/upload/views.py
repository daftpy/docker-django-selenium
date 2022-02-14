from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from .forms import CommentForm, UploadFileForm, LinkSubmissionForm
from .models import Comment, FileSubmission, LinkSubmission

def image_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                instance = FileSubmission(
                    title=request.POST['title'],
                    file=request.FILES['file'],
                    description=request.POST['description'],
                    private=form.cleaned_data['private'],
                    author=request.user
                )
                instance.save()
                return redirect(reverse(
                    'upload:submission', kwargs={
                        'submission_id': instance.id,
                        'submission_type': 'file'
                    }
                ))
        form = UploadFileForm()
        return render(request, "upload.html", {'form': form})
    else:
        return redirect(reverse('main:register'))

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
