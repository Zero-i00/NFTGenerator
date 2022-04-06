from itertools import product

from django import forms
from django.forms import Form, ModelForm

from NFTcore.models import User, FileGroup


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

# class FileFieldForm(Form):
#     attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
#     project_name = forms.CharField(max_length=255)
#     product_description = forms.CharField(max_length=5000)
#     collection_size = forms.IntegerField()
#     dimension_1 = forms.IntegerField()
#     dimension_2 = forms.IntegerField()
#     layer_name = forms.CharField(max_length=255)

class FileGroupForm(Form):
    layer_name = forms.CharField(max_length=255)
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'placeholder': 'New Layer'}))

class ScriptDataForm(Form):
    project_name = forms.CharField(max_length=255, required=False) #required=False
    product_description = forms.CharField(max_length=5000, required=False)
    collection_size = forms.IntegerField(required=False)
    dimension_1 = forms.IntegerField(required=False)
    dimension_2 = forms.IntegerField(required=False)