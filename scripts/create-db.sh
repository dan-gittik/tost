#!/bin/bash

set -e
cd "$(dirname ${BASH_SOURCE[0]})/.."

.env/bin/python manage.py makemigrations
.env/bin/python manage.py migrate
.env/bin/python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_user('admin', password='1234')
    user.is_superuser=True
    user.is_staff=True
    user.save()
EOF
