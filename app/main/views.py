from itertools import chain
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.db.models import CharField, Value
from upload.models import FileSubmission, LinkSubmission
from .forms import RegistrationForm

def index(request):
    # We get a list of file submissions and use annotate to add a
    # submission_type field with the value 'file'. This is used to help
    # build dynamic urls in the template.
    file_submission_list = FileSubmission.objects.filter(
            private=False
        ).order_by(
            '-created_at'
        ).annotate(
            submission_type=Value('file', output_field=CharField()
        )
    )
    # We do the same as above for link submissions.
    link_submission_list = LinkSubmission.objects.filter(
            private=False
        ).order_by(
            '-created_at'
        ).annotate(
            submission_type=Value('link', output_field=CharField()
        )
    )

    # Combine the link submission and file submission querysets
    # order by created_at and reverse the list.
    result_list = sorted(
        chain(
            file_submission_list,
            link_submission_list
        ),
        key=lambda instance: instance.created_at,
        reverse=True
    )

    return render(request, "main/index.html", {
        'submission_list': result_list
    })

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('main:index')
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {'form': form})
