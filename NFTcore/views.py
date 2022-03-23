import os, zipfile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout



class Home(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            download_files = request.GET.get('download-files')

            if download_files:
                file_paths = list()

                for root, directories, files in os.walk('./NFTcore/image_output'):
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
