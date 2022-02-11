from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

from .forms import CommentForm, UploadFileForm
from .models import Comment, FileSubmission

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
                    'upload:submission', kwargs={'submission_id': instance.id}
                ))
        form = UploadFileForm()
        return render(request, "upload.html", {'form': form})
    else:
        return redirect(reverse('main:register'))

def submission(request, submission_id):
    submission = get_object_or_404(FileSubmission, pk=submission_id)
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
                'upload:submission', kwargs={'submission_id': submission_id}
            ))
    form = CommentForm()
    return render(request, 'submission.html', {
        'submission': submission,
        'form': form,
        'comments': commentList
    })
