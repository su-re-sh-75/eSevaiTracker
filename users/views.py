from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        phone_num = password = request.POST.get('phone_num')
        user = authenticate(request, phone_num=phone_num, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!', 'info')
            # return redirect('/dashboard/')
            return HttpResponse("Login success")
        else:
            messages.error(request, 'Invalid phone number or password.', 'error')
    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        phone_num = password = request.POST.get('phone_num')
        name = request.POST.get('name', None)

        if User.objects.filter(phone_num=phone_num).exists():
            messages.error(request, 'Phone number already registered.', 'error')
        else:
            user = User.objects.create_user(phone_num=phone_num, name=name, password=password)
            messages.success(request, 'Account created successfully!', 'info')
            login(request, user)
            # return redirect('/dashboard/')
            return HttpResponse("Account created successfully!")

    return render(request, 'users/signup.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Log out Success', 'info')
    return redirect('/')
