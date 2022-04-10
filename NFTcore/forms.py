import os
from itertools import product

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import Form, ModelForm, FileInput

from NFTcore.models import *


class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class FileGroupForm(Form):
    # layer_name = forms.CharField(max_length=255)
    attachments = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'multiple': True, 'placeholder': 'New Layer', 'accept': 'application/png, application/jpg'}))


class ScriptDataForm(Form):
    project_name = forms.CharField(max_length=255) #, required=False
    product_description = forms.CharField(max_length=5000)
    collection_size = forms.IntegerField(min_value=1, max_value=150000)
    dimension_1 = forms.IntegerField(min_value=1)
    dimension_2 = forms.IntegerField(min_value=1)


class RarityForm(Form):
    body_only = forms.IntegerField(min_value=1, max_value=100)
    body_skin_clothes = forms.IntegerField(min_value=1, max_value=100)
    skin_body_without_clothes = forms.IntegerField(min_value=1, max_value=100)
    hair_only = forms.IntegerField(min_value=1, max_value=100)
    caps_only = forms.IntegerField(min_value=1, max_value=100)
    no_hair_no_caps = forms.IntegerField(min_value=1, max_value=100)
    hat = forms.IntegerField(min_value=1, max_value=100)
    accessories = forms.IntegerField(min_value=1, max_value=100)
    ears = forms.IntegerField(min_value=1, max_value=100)
    neck = forms.IntegerField(min_value=1, max_value=100)

