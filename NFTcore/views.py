import json
import os
import shutil
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
from scripts.nft_generator import check_paths, make_art
from django.views.generic.edit import FormView
from .forms import *
from .models import *
from .tasks import start_generate_nft, hello
from celery.result import AsyncResult


class Home(TemplateView):
    template_name = 'home/home.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # cards = CourseCard.objects.all()

            return render(request, self.template_name, {
                # 'cards': cards,
            })
        else:
            return redirect('login/')



def save_to_path(folder, folder_name, file_list):
    file_count = 1
    for element in file_list:
        path = default_storage.save(f'./Input/{folder}.{folder_name}/{file_count}.png', ContentFile(element.read()))
        export_img = os.path.join(f'Input{folder}.{folder_name}', path)
        file_count += 1

class FileFieldView(FormView):
    # form_class = FileFieldForm
    template_name = 'create/create_nft.html'  # Replace with your template.
    params_dict = {}
    rarity_dict = {}

    def get(self, request):
        background_form = FileGroupForm(self.request.GET or None)
        rare_background_form = FileGroupForm(self.request.GET or None)
        member_form = FileGroupForm(self.request.GET or None)
        pants_form = FileGroupForm(self.request.GET or None)
        clothes_form = FileGroupForm(self.request.GET or None)
        expresion_form = FileGroupForm(self.request.GET or None)
        vr_form = FileGroupForm(self.request.GET or None)
        hair_form = FileGroupForm(self.request.GET or None)
        head_form = FileGroupForm(self.request.GET or None)

        script_data_form = ScriptDataForm(self.request.GET or None)
        all_layers = LayerGroup.objects.all()




        rarity_form = RarityForm(self.request.GET or None)

        return render(request, self.template_name, {
            'background_form': background_form,
            'rare_background_form': rare_background_form,
            'script_data_form': script_data_form,
            'all_layers': all_layers,
            'member_form': member_form,
            'pants_form': pants_form,
            'clothes_form': clothes_form,
            'expresion_form': expresion_form,
            'vr_form': vr_form,
            'hair_form': hair_form,
            'head_form': head_form,
            'rarity_form': rarity_form
        })

    def post(self, request, *args, **kwargs):
        global collection_name, collection_description, number_of_combinations, width, height
        # shutil.rmtree('./Output/generated_images')


        background_form = FileGroupForm(request.POST, request.FILES)
        rare_background_form = FileGroupForm(request.POST, request.FILES)
        member_form = FileGroupForm(request.POST, request.FILES)
        pants_form = FileGroupForm(request.POST, request.FILES)
        clothes_form = FileGroupForm(request.POST, request.FILES)
        expresion_form = FileGroupForm(request.POST, request.FILES)
        vr_form = FileGroupForm(request.POST, request.FILES)
        hair_form = FileGroupForm(request.POST, request.FILES)
        head_form = FileGroupForm(request.POST, request.FILES)

        background_files = request.FILES.getlist('background_form')
        rare_background_files = request.FILES.getlist('rare_background_form')
        member_files = request.FILES.getlist('member_form')
        pants_files = request.FILES.getlist('pants_form')
        clothes_files = request.FILES.getlist('clothes_form')
        expresion_files = request.FILES.getlist('expresion_form')
        vr_files = request.FILES.getlist('vr_form')
        hair_files = request.FILES.getlist('hair_form')
        head_files = request.FILES.getlist('head_form')

        save_to_path('01', 'Background', background_files)
        save_to_path('02', 'Rare Background', rare_background_files)
        save_to_path('03', 'Member', member_files)
        save_to_path('04', 'Pants', pants_files)
        save_to_path('05', 'Clothes', clothes_files)
        save_to_path('06', 'Expresion', expresion_files)
        save_to_path('07', 'Vr', vr_files)
        save_to_path('08', 'Hair', hair_files)
        save_to_path('09', 'Head', head_files)

        rarity_form = RarityForm(request.POST)

        if rarity_form.is_valid():
            self.rarity_dict['body_only'] = rarity_form['body_only'].value(),
            self.rarity_dict['body_skin_clothes'] = rarity_form['body_skin_clothes'].value()
            self.rarity_dict['skin_body_without_clothes'] = rarity_form['skin_body_without_clothes'].value()
            self.rarity_dict['hair_only'] = rarity_form['hair_only'].value()
            self.rarity_dict['caps_only'] = rarity_form['caps_only'].value()
            self.rarity_dict['no_hair_no_caps'] = rarity_form['no_hair_no_caps'].value()
            self.rarity_dict['hat'] = rarity_form['hat'].value()
            self.rarity_dict['accessories'] = rarity_form['accessories'].value()
            self.rarity_dict['ears'] = rarity_form['ears'].value()
            self.rarity_dict['neck'] = rarity_form['neck'].value()


        script_data_form = ScriptDataForm(request.POST)
        all_layers = LayerGroup.objects.all()


        if script_data_form.is_valid():

            self.params_dict['collection_name'] = script_data_form['project_name'].value(),
            self.params_dict['collection_description'] = script_data_form['product_description'].value(),
            self.params_dict['number_of_combinations'] = script_data_form['collection_size'].value(),
            self.params_dict['width'] = script_data_form['dimension_1'].value(),
            self.params_dict['height'] = script_data_form['dimension_2'].value(),

            with open('params.json', 'w') as file:
                json.dump(self.params_dict, file)

            with open('rarity.json', 'w') as file:
                json.dump(self.rarity_dict, file)

            # start_generate_nft.delay()
            task = start_generate_nft.delay()
            messages.info(request, 'Your collection is being generated. It might take a couple of hours')
            task_id = task.task_id
            res = AsyncResult(task_id)
            print(res.ready())
            if res.ready() == False:
                return redirect('/download-img/')
            # print(self.params_dict)

            # with open('params.json', 'w') as file:
            #     json.dump(self.params_dict, file)
            #
            # with open('rarity.json', 'w') as file:
            #     json.dump(self.rarity_dict, file)
            #
            # check_paths()
            # export_path_for_meta_data_global = os.path.join(os.getcwd(), 'Output', '_metadata', '_metadata.json')
            #
            # with open(export_path_for_meta_data_global, 'a') as f:
            #     f.write('[\n')
            # make_art()
            # with open(export_path_for_meta_data_global, 'a') as f:
            #     f.write(']')


        return render(request, self.template_name, {
            'background_form': background_form,
            'rare_background_form': rare_background_form,
            'member_form': member_form,
            'pants_form': pants_form,
            'clothes_form': clothes_form,
            'expresion_form': expresion_form,
            'vr_form': vr_form,
            'hair_form': hair_form,
            'head_form': head_form,
            'script_data_form': script_data_form,
            'all_layers': all_layers,

            'rarity_form': rarity_form,
        })



# class PreviewView(FormView):
#
#     template_name = 'create/preview.html'
#
#     def get(self, request):
#         script_data_form = ScriptDataForm(self.request.GET or None)
#
#         all_layers = LayerGroup.objects.all()
#         generated_img = 'scripts/Output/generated_images/1.png'
#         media_path = 'static/generated_img/1.png'
#
#
#         shutil.copy2(generated_img, media_path)
#
#         return render(request, self.template_name, {
#             'script_data_form': script_data_form,
#             'all_layers': all_layers,
#             'preview_img': generated_img,
#         })
#
#     def post(self, request, *args, **kwargs):
#
#
#         script_data_form = ScriptDataForm(request.POST)
#         all_layers = LayerGroup.objects.all()
#
#         if script_data_form.is_valid():
#
#             # file_count = 1
#
#             # if not os.path.exists('scripts/Input'):
#             #     os.mkdir('scripts/Input')
#             # check_paths()
#             # export_path_for_meta_data_global = os.path.join('scripts', 'Output', '_metadata', '_metadata.json')
#             # with open(export_path_for_meta_data_global, 'a') as f:
#             #     f.write('[\n')
#
#             collection_name = script_data_form['project_name'].value()
#             collection_description = script_data_form['product_description'].value()
#             number_of_combinations = script_data_form['collection_size'].value()
#             width = script_data_form['dimension_1'].value()
#             height = script_data_form['dimension_2'].value()
#
#             users_file_group = LayerGroup.objects.filter(user=request.user)
#
#             # for image in users_file_group:
#             #     all_images = File.objects.filter(fg=image)  # file list
#             #     for file in all_images:
#             #         if not os.path.exists(f'scripts/Input/0{file_count}'):
#             #             path = os.mkdir(f'scripts/Input/0{file_count}')
#             #             file = str(file.file).split('/')[-1]
#             #             os.replace('media/scripts/Input/' + file, f'scripts/Input/0{file_count}/' + file)
#             #         else:
#             #             file = str(file.file).split('/')[-1]
#             #             os.path.join(f'scripts/Input/0{file_count}/', file)
#             #
#             #         make_art(project_name, product_description, collection_size, dimension_1, dimension_2)
#             #         with open(export_path_for_meta_data_global, 'a') as f:
#             #             f.write(']')
#             #     file_count += 1
#
#                 # return redirect('/download-img/')
#
#         return render(request, self.template_name, {
#             'script_data_form': script_data_form,
#             'all_layers': all_layers,
#         })





class GeneratedImageView(TemplateView):

    template_name = 'generated/generated.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            return render(request, self.template_name, {})
        else:
            return redirect('login/')

    def post(self, request):
        if 'download-zip' in request.POST:

            file_paths = list()

            for root, directories, files in os.walk('./Output/'):
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

            FileGroup.objects.all().delete



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
