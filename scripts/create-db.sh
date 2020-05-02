#!/bin/bash

set -e
cd "$(dirname ${BASH_SOURCE[0]})/.."

.env/bin/python manage.py makemigrations
.env/bin/python manage.py migrate
.env/bin/python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_user(
        username = 'admin',
        password = '1234',
        is_staff = True,
        is_superuser = True,
    )
    user.save()
EOF
.env/bin/python manage.py shell <<EOF
from website.models import Settings
Settings.objects.get_or_create()
EOF
