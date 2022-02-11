from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from upload.models import FileSubmission
from .forms import RegistrationForm

# Create your views here.
def index(request):
    submission_list = FileSubmission.objects.filter(private=False).order_by('-created_at')
    return render(request, "main/index.html", {'submission_list': submission_list})

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
