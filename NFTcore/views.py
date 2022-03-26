import os
import zipfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
import shutil
from scripts.nft_generator import check_paths, make_art
from django.views.generic.edit import FormView
from .forms import FileFieldForm, UserRegistrationForm


class Home(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            download_files = request.GET.get('download-files')

            if download_files:
                file_paths = list()

                for root, directories, files in os.walk('./scripts/Output/'):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        file_paths.append(filepath)

                with zipfile.ZipFile('file.zip', 'w') as zip:
                    for file in file_paths:
                        zip.write(file, os.path.basename(file))

                with open('file.zip', 'rb') as file:
                    response = HttpResponse(file, content_type='application/force-download')
                    response['Content-Disposition'] = 'attachment; filename=file_nft.zip'
                    return response

            return render(request, self.template_name, {})
        else:
            return redirect('login/')



class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'create/create_nft.html'  # Replace with your template.
    success_url = '/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        if os.path.exists('scripts/Input'):
            shutil.rmtree('scripts/Input')
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        files = request.FILES.getlist('attachments')
        collection_name = request.POST.get('collection_name')
        collection_description = request.POST.get('collection_description')
        file_count = 1

        if not os.path.exists('scripts/Input'):
            os.mkdir('scripts/Input')
        check_paths()
        export_path_for_meta_data_global = os.path.join('scripts', 'Output', '_metadata', '_metadata.json')
        with open(export_path_for_meta_data_global, 'a') as f:
            f.write('[\n')

        if form.is_valid():
            for f in files:
                if not os.path.exists(f'scripts/Input/0{file_count}'):
                    path = os.mkdir(f'scripts/Input/0{file_count}')

                img = default_storage.save(f'scripts/Input/0{file_count}/nft_img{file_count}.png', ContentFile(f.read()))
                file_count += 1

            make_art(collection_name, collection_description)
            with open(export_path_for_meta_data_global, 'a') as f:
                f.write(']')

            return self.form_valid(form)
        else:
            return self.form_invalid(form)



def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)


        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Incorrect data')

    context = {}
    return render(request, 'login/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/')
