# Generated by Django 3.0.5 on 2020-05-02 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='github',
            new_name='github_username',
        ),
    ]
