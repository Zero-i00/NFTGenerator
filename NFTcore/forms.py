from django import forms
from django.forms import Form, ModelForm

from NFTcore.models import User


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class FileFieldForm(Form):
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    collection_name = forms.CharField(max_length=255)
    collection_description = forms.CharField(max_length=255)