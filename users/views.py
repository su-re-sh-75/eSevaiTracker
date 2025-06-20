from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

def login_view(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(request, phone_num=phone_num, password=password)

        if user is not None:
            if user_type == 'customer' and not user.is_staff:
                login(request, user)
                messages.success(request, 'Customer login success!', 'info')
                return redirect('/dashboard/')
            elif user_type == 'staff' and user.is_staff:
                login(request, user)
                messages.success(request, 'Staff login success!', 'info')
                return redirect('/staff/dashboard/')
            else:
                messages.error(request, 'User type mismatch.', 'error')
        else:
            messages.error(request, 'Invalid phone number or password.', 'error')

    return render(request, 'users/login.html')


def signup_view(request):
    if request.method == 'POST':
        phone_num = request.POST.get('phone_num')
        password = request.POST.get('password')
        name = request.POST.get('name')
        user_type = request.POST.get('user_type')

        if User.objects.filter(phone_num=phone_num).exists():
            messages.error(request, 'Phone number already registered.', 'error')
        else:
            is_staff = True if user_type == 'staff' else False
            user = User.objects.create_user(phone_num=phone_num, name=name, password=password)
            user.is_staff = is_staff
            user.save()
            login(request, user)
            messages.success(request, f'{user_type.capitalize()} account created successfully!', 'info')
            if user.is_staff:
                return redirect('/staff/dashboard/')
            else:
                return redirect('/dashboard/')
            
    return render(request, 'users/signup.html')


@login_required
def logout_view(request):
    user = request.user
    logout(request)
    messages.success(request, f'Logged out {user.phone_num} successfully!', 'info')
    return redirect('/users/login/')
