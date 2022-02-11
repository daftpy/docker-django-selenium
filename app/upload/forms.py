from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField()
    description = forms.CharField(widget=forms.Textarea)
    private = forms.BooleanField(initial=False, required=False)
    permission = forms.BooleanField(initial=False, required=True)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
