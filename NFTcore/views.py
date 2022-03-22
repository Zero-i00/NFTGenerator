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
