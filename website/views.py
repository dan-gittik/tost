import secrets

from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from . import models


# VIEWS


def index(request):
    return render(request, 'index.html')


def register(request):
    settings = models.Settings.get()
    if request.method == 'POST':
        try:
            user = register_user(request, settings)
            return render(request, 'register_success.html')
        except ValueError as error:
            return render(request, 'register.html', {
                'error': error,
                'values': request.POST,
                'settings': settings,
            })
    return render(request, 'register.html', {
        'settings': settings,
    })


def login(request):
    if request.method == 'POST':
        try:
            login_user(request)
            return redirect(request.GET.get('next', 'account'))
        except ValueError as error:
            return render(request, 'login.html', {
                'error': error,
                'values': request.POST,
            })
    return render(request, 'login.html')


def reset_password(request):
    if request.method == 'POST':
        pass
    return render(request, 'reset_password.html')


@login_required
def account(request):
    if request.method == 'POST':
        try:
            update_password(request)
        except ValueError as error:
            return render(request, 'account.html', {
                'error': error,
                'values': request.POST,
                'user': request.user,
            })
    return render(request, 'account.html', {
        'user': request.user,
    })


def logout(request):
    do_logout(request)
    return redirect('index')


@login_required
def delete_account(request):
    request.user.delete()
    do_logout(request)
    return redirect('index')


def validate_email(request):
    token = request.GET.get('token')
    error = render(request, 'validate_email.html', {
        'error': 'Invalid token.',
    })
    if not token:
        return error
    user = User.objects.filter(last_name=token).first()
    if not user:
        return error
    user.last_name = ''
    user.is_active = True
    user.save()
    do_login(request, user)
    return redirect(request.GET.get('next', 'account'))


# HELPERS


def register_user(request, settings):
    if settings.token:
        token = request.POST.get('token')
        if token != settings.token:
            raise ValueError('Invalid token.')
    student_id = request.POST.get('student_id')
    if not is_valid_student_id(student_id):
        raise ValueError('Invalid student ID.')
    name = request.POST.get('name')
    if not name:
        raise ValueError('Invalid name.')
    email = request.POST.get('email')
    if not is_valid_email(email):
        raise ValueError('Invalid email address.')
    password = request.POST.get('password')
    if not is_valid_password(password):
        raise ValueError('Invalid password.')
    if User.objects.filter(username=student_id).exists():
        raise ValueError('A student with this ID already exists')
    if User.objects.filter(email=email).exists():
        raise ValueError('A student with this email already exists')
    token = secrets.token_urlsafe(64)
    print(token)
    user = User.objects.create_user(
        username = student_id,
        first_name = name,
        last_name = token,
        email = email,
        password = password,
        is_active = False,
    )
    # Send validation email.
    return user


def login_user(request):
    email = request.POST.get('email')
    if not is_valid_email(email):
        raise ValueError('Invalid email.')
    password = request.POST.get('password')
    if not is_valid_password(password):
        raise ValueError('Invalid password.')
    user = User.objects.filter(email=email).first()
    if not user or not user.is_active:
        raise ValueError('Your email has not been validated yet.')
    if user.check_password(password):
        do_login(request, user)
        return user
    raise ValueError('Invalid credentials.')


def update_password(request):
    password = request.POST.get('password')
    if not is_valid_password(password):
        raise ValueError('Invalid password.')
    request.user.set_password(password)
    request.user.save()


def is_valid_student_id(student_id):
    return student_id and student_id.isnumeric()


def is_valid_email(email):
    return email and '@' in email


def is_valid_password(password):
    return password
