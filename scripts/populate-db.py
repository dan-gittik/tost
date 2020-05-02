#!/usr/bin/env python

import os
import pathlib
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
sys.path.append(str(pathlib.Path(__file__).absolute().parent.parent))

import django

django.setup()

import datetime as dt

from django.contrib.auth.models import User as AuthUser
from website.models import User, Exercise, Extension


def main():
    for i in range(10):
        email = f'{i}@gmail.com'
        student_id = f'{i}' * 5
        if not User.objects.filter(student_id=student_id).exists():
            auth = AuthUser.objects.create_user(
                username = email,
                password = f'{i}' * 3,
            )
            user = User.objects.create(
                auth = auth,
                name = f'user {i}',
                email = email,
                student_id = student_id,
                github_username = f'user{i}',
                is_valid = True,
            )
    today = dt.date.today()
    for i in range(10):
        title = f'exercise {i}'
        if not Exercise.objects.filter(title=title).exists():
            offset = 2 * (i - 5)
            exercise = Exercise.objects.create(
                title = title,
                number = i,
                directory = f'exercise{i}',
                repo_url = f'https://github.com/{i}',
                instructions_url = f'https://docs.google.com/{i}',
                publish_date = today + dt.timedelta(days=offset),
                deadline = today + dt.timedelta(days=offset + 7),
            )
            if i % 3 == 2:
                extension = Extension.objects.create(
                    user = User.objects.get(student_id='11111'),
                    exercise = exercise,
                    deadline = today + dt.timedelta(days=offset + 10),
                    reason = f'reason {i}',
                    status = Extension.APPROVED,
                )



if __name__ == '__main__':
    main()
