import os
import shutil
import zipfile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from scripts.nft_generator import check_paths, make_art
from django.views.generic.edit import FormView
from .forms import FileGroupForm, ScriptDataForm
from .models import *
from .services import test


class Home(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # download_files = request.GET.get('download-files')
            #
            cards = CourseCard.objects.all()
            #
            # # test.delay()
            # if download_files:
            #     file_paths = list()
            #
            #     for root, directories, files in os.walk('./scripts/Output/'):
            #         for filename in files:
            #             filepath = os.path.join(root, filename)
            #             file_paths.append(filepath)
            #
            #     with zipfile.ZipFile('file.zip', 'w') as zip:
            #         for file in file_paths:
            #             zip.write(file, os.path.basename(file))
            #
            #     with open('file.zip', 'rb') as file:
            #         response = HttpResponse(file, content_type='application/force-download')
            #         response['Content-Disposition'] = 'attachment; filename=file_nft.zip'
            #         return response

            return render(request, self.template_name, {
                'cards': cards,
            })
        else:
            return redirect('login/')



class FileFieldView(FormView):
    # form_class = FileFieldForm
    template_name = 'create/create_nft.html'  # Replace with your template.


    def get(self, request):
        file_group_form = FileGroupForm(self.request.GET or None)
        script_data_form = ScriptDataForm(self.request.GET or None)

        all_layers = FileGroup.objects.all()

        return render(request, self.template_name, {
            'file_group_form': file_group_form,
            'script_data_form': script_data_form,
            'all_layers': all_layers,
        })

    def post(self, request, *args, **kwargs):

        file_group_form = FileGroupForm(request.POST, request.FILES)
        script_data_form = ScriptDataForm(request.POST)

        all_layers = FileGroup.objects.all()

        files = request.FILES.getlist('attachments')

        if 'create-layer' in request.POST:
            if file_group_form.is_valid():
                group = FileGroup.objects.create(user=request.user, layer_name=file_group_form.cleaned_data['layer_name'])

                for image in files:
                    file = File(fg=group, file=image)
                    file.save()

        if script_data_form.is_valid():

            file_count = 1

            if not os.path.exists('scripts/Input'):
                os.mkdir('scripts/Input')
            check_paths()
            export_path_for_meta_data_global = os.path.join('scripts', 'Output', '_metadata', '_metadata.json')
            with open(export_path_for_meta_data_global, 'a') as f:
                f.write('[\n')

            project_name = script_data_form['project_name'].value()
            product_description = script_data_form['product_description'].value()
            collection_size = script_data_form['collection_size'].value()
            dimension_1 = script_data_form['dimension_1'].value()
            dimension_2 = script_data_form['dimension_2'].value()

            users_file_group = FileGroup.objects.filter(user=request.user)

            for image in users_file_group:
                all_images = File.objects.filter(fg=image) # file list
                for file in all_images:
                    if not os.path.exists(f'scripts/Input/0{file_count}'):
                        path = os.mkdir(f'scripts/Input/0{file_count}')
                        file = str(file.file).split('/')[-1]
                        os.replace('media/scripts/Input/' + file, f'scripts/Input/0{file_count}/' + file)
                    else:
                        file = str(file.file).split('/')[-1]
                        os.path.join(f'scripts/Input/0{file_count}/', file)
                file_count += 1



            if 'preview-collection' in request.POST:
                make_art(project_name, product_description, 1, dimension_1, dimension_2)
                print('preview')
                return redirect('/collection-preview/')
            elif 'generate-full-collection' in request.POST:
                make_art(project_name, product_description, collection_size, dimension_1, dimension_2)
                print('all-collection')
                return redirect('/')
            with open(export_path_for_meta_data_global, 'a') as f:
                f.write(']')


        return render(request, self.template_name, {
            'file_group_form': file_group_form,
            'script_data_form': script_data_form,
            'all_layers': all_layers,
        })



class PreviewView(FormView):

    template_name = 'create/preview.html'

    def get(self, request):
        script_data_form = ScriptDataForm(self.request.GET or None)

        all_layers = FileGroup.objects.all()
        generated_img = 'scripts/Output/generated_images/1.png'
        media_path = 'static/generated_img/1.png'


        shutil.copy2(generated_img, media_path)

        return render(request, self.template_name, {
            'script_data_form': script_data_form,
            'all_layers': all_layers,
            'preview_img': generated_img,
        })

    def post(self, request, *args, **kwargs):


        script_data_form = ScriptDataForm(request.POST)
        all_layers = FileGroup.objects.all()

        if script_data_form.is_valid():

            file_count = 1

            if not os.path.exists('scripts/Input'):
                os.mkdir('scripts/Input')
            check_paths()
            export_path_for_meta_data_global = os.path.join('scripts', 'Output', '_metadata', '_metadata.json')
            with open(export_path_for_meta_data_global, 'a') as f:
                f.write('[\n')

            project_name = script_data_form['project_name'].value()
            product_description = script_data_form['product_description'].value()
            collection_size = script_data_form['collection_size'].value()
            dimension_1 = script_data_form['dimension_1'].value()
            dimension_2 = script_data_form['dimension_2'].value()

            users_file_group = FileGroup.objects.filter(user=request.user)

            for image in users_file_group:
                all_images = File.objects.filter(fg=image)  # file list
                for file in all_images:
                    if not os.path.exists(f'scripts/Input/0{file_count}'):
                        path = os.mkdir(f'scripts/Input/0{file_count}')
                        file = str(file.file).split('/')[-1]
                        os.replace('media/scripts/Input/' + file, f'scripts/Input/0{file_count}/' + file)
                    else:
                        file = str(file.file).split('/')[-1]
                        os.path.join(f'scripts/Input/0{file_count}/', file)

                    make_art(project_name, product_description, collection_size, dimension_1, dimension_2)
                    with open(export_path_for_meta_data_global, 'a') as f:
                        f.write(']')
                file_count += 1

                return redirect('/')

        return render(request, self.template_name, {
            'script_data_form': script_data_form,
            'all_layers': all_layers,
        })

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
