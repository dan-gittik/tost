import secrets

from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from . import models


# VIEWS


def index(request):
    return render(request, 'index.html')


def register(request):
    settings = models.Settings.get()
    if request.method == 'POST':
        try:
            user = _register_user(request, settings)
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
    if request.user.is_authenticated:
        return redirect('account')
    if request.method == 'POST':
        try:
            _login_user(request)
            return redirect(request.GET.get('next') or 'account')
        except ValueError as error:
            return render(request, 'login.html', {
                'error': error,
                'values': request.POST,
            })
    return render(request, 'login.html')


def reset_password(request):
    if request.method == 'POST':
        try:
            _reset_password(request)
            return render(request, 'reset_password_success.html')
        except ValueError as error:
            return render(request, 'reset_password.html', {
                'error': error,
                'values': request.POST,
            })
    return render(request, 'reset_password.html')


@login_required
def account(request):
    if request.method == 'POST':
        try:
            _update_password(request)
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
    try:
        _validate_email(request)
    except ValueError as error:
        return render(request, 'validate_email.html', {
            'error': error,
        })
    return redirect(request.GET.get('next') or 'account')


@csrf_exempt
def change_password(request):
    args = request.POST if request.method == 'POST' else request.GET
    email = args.get('email')
    token = args.get('token')
    if not email or not token:
        return redirect('index')
    user = User.objects.filter(email=email, last_name=token).first()
    if not user:
        return redirect('index')
    if request.method == 'POST':
        try:
            _update_password(request, user=user)
            return redirect(request.POST.get('next') or 'account')
        except ValueError as error:
            return render(request, 'change_password.html', {
                'error': error,
                'values': request.POST,
            })
    return render(request, 'change_password.html', {
        'user': user,
        'values': request.GET,
    })


# HELPERS


def _register_user(request, settings):
    if settings.token:
        token = request.POST.get('token')
        if token != settings.token:
            raise ValueError('Invalid token.')
    student_id = request.POST.get('student_id')
    if not _is_valid_student_id(student_id):
        raise ValueError('Invalid student ID.')
    name = request.POST.get('name')
    if not name:
        raise ValueError('Invalid name.')
    email = request.POST.get('email')
    if not _is_valid_email(email):
        raise ValueError('Invalid email address.')
    password = request.POST.get('password')
    if not _is_valid_password(password):
        raise ValueError('Invalid password.')
    if User.objects.filter(username=student_id).exists():
        raise ValueError('A student with this ID already exists')
    if User.objects.filter(email=email).exists():
        raise ValueError('A student with this email already exists')
    token = secrets.token_urlsafe(64)
    print(token) # TODO send email.
    user = User.objects.create_user(
        username = student_id,
        first_name = name,
        last_name = token,
        email = email,
        password = password,
        is_active = False,
    )
    return user


def _login_user(request):
    email = request.POST.get('email')
    if not _is_valid_email(email):
        raise ValueError('Invalid email.')
    password = request.POST.get('password')
    if not _is_valid_password(password):
        raise ValueError('Invalid password.')
    user = User.objects.filter(email=email).first()
    if not user or not user.is_active:
        raise ValueError('Your email has not been validated yet.')
    if user.check_password(password):
        do_login(request, user)
        return user
    raise ValueError('Invalid credentials.')


def _update_password(request, user=None):
    if not user:
        user = request.user
    password = request.POST.get('password')
    if not _is_valid_password(password):
        raise ValueError('Invalid password.')
    user.set_password(password)
    user.last_name = ''
    user.save()
    do_login(request, user)


def _reset_password(request):
    email = request.POST.get('email')
    if not _is_valid_email(email):
        raise ValueError('Invalid email.')
    user = User.objects.filter(email=email).first()
    if user and user.is_active:
        token = secrets.token_urlsafe(64)
        print(token) # TODO send email.
        user.last_name = token
        user.save()


def _validate_email(request):
    token = request.GET.get('token')
    if not token:
        raise ValueError('Invalid token.')
    user = User.objects.filter(last_name=token).first()
    if not user:
        return error
    user.last_name = ''
    user.is_active = True
    user.save()
    do_login(request, user)




def _is_valid_student_id(student_id):
    return student_id and student_id.isnumeric()


def _is_valid_email(email):
    return email and '@' in email


def _is_valid_password(password):
    return password
