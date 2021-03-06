import datetime as dt
import secrets

import dateutil.parser as dateutil
from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect

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


@login_required
def exercises(request):
    today = timezone().now().date()
    exercises = models.UserExercise.all(request.user, today)
    return render(request, 'exercises.html', {
        'today': today,
        'exercises': exercises,
        'Extension': models.Extension,
    })


@login_required
def exercise_test(request, exercise):
    pass


@login_required
def exercise_cr_files(request, exercise, path):
    pass


@login_required
def forum(request, exercise):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    return render(request, 'forum.html', {
        'exercise': exercise,
    })


@login_required
def add_post(request, exercise):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    if request.method == 'POST':
        try:
            post = _add_post(request, exercise)
            return redirect('post', exercise.order, post.pk)
        except ValueError as error:
            return render(request, 'edit_post.html', {
                'error': error,
                'exercise': exercise,
                'post': request.POST,
            })
    return render(request, 'edit_post.html', {
        'exercise': exercise,
    })


@login_required
def post(request, exercise, post):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    post = get_object_or_404(models.Post, pk=post)
    return render(request, 'post.html', {
        'exercise': exercise,
        'post': post,
    })


@login_required
def edit_post(request, exercise, post):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    post = get_object_or_404(models.Post, pk=post)
    if request.method == 'POST':
        try:
            _edit_post(request, post)
            return redirect('post', exercise.order, post.pk)
        except ValueError as error:
            return render(request, 'edit_post.html', {
                'error': error,
                'exercise': exercise,
                'post': post,
                'values': request.POST,
            })
    return render(request, 'edit_post.html', {
        'exercise': exercise,
        'post': post,
    })


@login_required
def delete_post(request, exercise, post):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    post = get_object_or_404(models.Post, pk=post)
    post.delete()
    return redirect('forum', exercise.pk)


@login_required
def add_comment(request, exercise, post):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    post = get_object_or_404(models.Post, pk=post)
    if request.method == 'POST':
        try:
            _add_comment(request, post)
        except ValueError as error:
            return render(request, 'post.html', {
                'error': error,
                'exercise': exercise,
                'post': post,
                'values': request.POST,
            })
    return redirect('post', exercise.order, post.pk)


@login_required
def edit_comment(request, exercise, post, comment):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    post = get_object_or_404(models.Post, pk=post)
    comment = get_object_or_404(models.Comment, pk=comment)
    if request.method == 'POST':
        try:
            _edit_comment(request, comment)
            return redirect('post', exercise.order, post.pk)
        except ValueError as error:
            return render(request, 'post.html', {
                'error': error,
                'exercise': exercise,
                'post': post,
                'target': comment,
                'values': request.POST,
            })
    return render(request, 'post.html', {
        'exercise': exercise,
        'post': post,
        'target': comment,
    })


@login_required
def delete_comment(request, exercise, post, comment):
    exercise = get_object_or_404(models.Exercise, order=exercise)
    post = get_object_or_404(models.Post, pk=post)
    comment = get_object_or_404(models.Comment, pk=comment)
    comment.delete()
    return redirect('post', exercise.pk, post.pk)


@login_required
def extension(request):
    if request.method == 'POST':
        _add_extension(request)
        return redirect('exercises')
    today = timezone.now().date()
    exercises = models.Exercise.objects.annotate(count=Count('extensions')).filter(
        publish_date__lte = today,
        deadline__gt = today,
        count = 0,
    )
    if not exercises.exists():
        return redirect('exercises')
    return render(request, 'extension.html', {
        'selected': int(request.GET.get('exercise')),
        'exercises': exercises,
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


def _add_extension(request):
    exercise = request.POST.get('exercise')
    if not _is_valid_exercise(exercise):
        raise ValueError('Invalid exercise.')
    deadline = request.POST.get('deadline')
    if not _is_valid_date(deadline):
        raise ValueError('Invalid date.')
    deadline = dateutil.parse(deadline).date()
    reason = request.POST.get('reason')
    if not reason:
        raise ValueError('Invalid reason.')
    exercise = models.Exercise.objects.filter(order=exercise).first()
    if models.Extension.objects.filter(user=request.user, exercise=exercise).exists():
        raise ValueError('Exercise already has an extension.')
    models.Extension.objects.create(
        user = request.user,
        exercise = exercise,
        deadline = deadline,
        reason = reason,
        status = models.Extension.PENDING,
    )


def _add_post(request, exercise):
    title = request.POST.get('title')
    if not title:
        raise ValueError('Invalid title.')
    content = request.POST.get('content')
    if not content:
        raise ValueError('Invalid content.')
    post = models.Post.objects.create(
        exercise = exercise,
        title = title,
        author = request.user,
        content = content,
    )
    return post


def _edit_post(request, post):
    title = request.POST.get('title')
    if not title:
        raise ValueError('Invalid title.')
    content = request.POST.get('content')
    if not content:
        raise ValueError('Invalid content.')
    post.title = title
    post.content = content
    post.save()


def _add_comment(request, post):
    content = request.POST.get('content')
    if not content:
        raise ValueError('Invalid content.')
    comment = models.Comment.objects.create(
        post = post,
        author = request.user,
        content = content,
    )
    return comment


def _edit_comment(request, comment):
    content = request.POST.get('content')
    if not content:
        raise ValueError('Invalid content.')
    comment.content = content
    comment.save()


def _is_valid_student_id(student_id):
    return student_id and student_id.isnumeric()


def _is_valid_email(email):
    return email and '@' in email


def _is_valid_password(password):
    return password


def _is_valid_exercise(exercise):
    if not exercise or not exercise.isnumeric():
        return False
    today = timezone.now().date()
    exercise = models.Exercise.objects.filter(
        order = int(exercise),
        publish_date__lte = today,
        deadline__gt = today,
    ).first()
    if not exercise:
        return False
    return True


def _is_valid_date(date):
    if not date:
        return False
    try:
        return isinstance(dateutil.parse(date), dt.datetime)
    except Exception:
        return False
