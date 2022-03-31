from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, VideoForm
from django.template.loader import get_template
from django.template import Context
from .models import Video
from django.shortcuts import render



#################### index#######################################
def index(request):
    return render(request, 'index.html', {'title': 'index'})

#################### index#######################################
def show(request):
    Videos = Video.objects.all()

    context = {'Videos': Videos}

    return render(request, 'videos.html', context)

#################### index#######################################
@login_required()
def upload(request):
    lastvideo = Video.objects.last()

    videofile = lastvideo.videofile

    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context = {'videofile': videofile,
               'form': form
               }

    return render(request, 'upload.html', context)


########### register here #####################################
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'title': 'reqister here'})


################ login forms###################################################
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account does not exit, plz sign in')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'log in'})
