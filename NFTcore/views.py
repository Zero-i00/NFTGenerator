import json
import time
import zipfile
from django.core.files import File as DjangoFile
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
from .tasks import start_generate_nft
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

def check_image_type(list):
    white_list = ['png', 'jpg', 'jpeg']
    for i in list:
        if str(i).split('.')[-1] in white_list:
            return True
        else:
            return False

class FileFieldView(FormView):
    # form_class = FileFieldForm
    template_name = 'create/create_nft.html'  # Replace with your template.
    params_dict = {}
    rarity_dict = {}

    def get(self, request):
        if Celery.objects.filter(user=User.objects.get(id=request.user.id)):
            return redirect('generation_progress')
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


        print(check_image_type(background_files))
        if check_image_type(background_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(rare_background_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(member_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(pants_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(clothes_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(expresion_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(vr_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(hair_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')
        elif check_image_type(head_files) == False:
            messages.error(request, 'Use the correct image format')
            return redirect('/create_collections/')


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

            task = start_generate_nft.delay()
            task_id = task.task_id
            res = AsyncResult(task_id)

            if res.ready() == False:
                Celery.objects.create(task_id=task_id, user=User.objects.get(id=request.user.id))
            check_paths()
            export_path_for_meta_data_global = os.path.join(os.getcwd(), 'Output', '_metadata', '_metadata.json')
            with open(export_path_for_meta_data_global, 'a') as f:
                f.write('[\n')
            make_art()
            with open(export_path_for_meta_data_global, 'a') as f:
                f.write(']')
            return redirect('/generation-in-progress/')

            # check_paths()
            # export_path_for_meta_data_global = os.path.join(os.getcwd(), 'Output', '_metadata', '_metadata.json')
            #
            # with open(export_path_for_meta_data_global, 'a') as f:
            #     f.write('[\n')
            # make_art()
            #
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


class GeneratedImageView(TemplateView):

    template_name = 'generated/generated.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            not_download = None
            if os.listdir('Output/generated_images') == []:
                not_download = True
                print(not_download)
            else:
                not_download = False
                print(not_download)
            return render(request, self.template_name, {
                'not_download': not_download,
            })
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


def generation_in_progress_view(request):
    #return render(request, 'generated/expectation.html', context={})

    try:
        celery = Celery.objects.get(user=request.user.id)
    except Celery.DoesNotExist:
        return redirect('create_collections')
    res = AsyncResult(str(celery.task_id))
    print(res.ready())
    print(res.state)
    if not res.ready():
        return render(request, 'generated/expectation.html', context={})
    else:
        return redirect('download-img')

def test_task_view(request):
    task = start_generate_nft.delay()
    task_id = task.task_id
    Celery.objects.create(task_id=task_id, user=User.objects.get(id=request.user.id))

class ProfileView(TemplateView):
    template_name = 'profile/index.html'

    def get(self, request):
        if request.user and request.user.is_authenticated:
            user = User.objects.get(email=request.user.email)
            users_collection = UsersCollection.objects.filter(user=request.user).first()
            return render(request, self.template_name, {
                'user': user,
                'users_collection': users_collection,
            })
        else:
            return redirect('login/')

    def post(self, request):
        if 'download-zip' in request.POST:
            # print('hello')
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
