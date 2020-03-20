from django.shortcuts import render, redirect
from .models import Document
from crud.forms import *
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings


@login_required
def fileupload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'File Uploaded successfully!')

            subject = 'File Uploaded successfully!'
            message = 'check folder, 1 new file added'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['agenzianapoli4@sailpost.it', 'tatumfgdillon@gmail.com']
            send_mail(subject, message, email_from, recipient_list)

        return redirect('home')
    else:
        form = DocumentForm()
        if request.user.is_superuser:
            documents = Document.objects.order_by('-uploaded_at')
        else:
            documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
        context = {
        'form':form,
        'documents': documents,
        }
    return render(request, 'fileupload.html', context)

@csrf_protect
def register(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    is_staff=True,
                    is_active=True,
                    is_superuser=False,
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                return redirect('index')
        else:
            form = RegistrationForm()
            return render(request, 'register.html', {'form': form})
    else:
        return redirect("index")

def register_success(request):
    return render(request, 'success.html')

@login_required
def users(request):
    users_list = User.objects.all()
    paginator = Paginator(users_list, 5)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'users.html', {'users': users})

@login_required
def user_delete(request, id):
    user = User.objects.get(id=id)
    user.delete()
    messages.error(request, 'User was deleted successfully!')
    return redirect('/users')

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = NewPassChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, ('Your password was successfully updated!'))
            return redirect('index')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form = NewPassChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
