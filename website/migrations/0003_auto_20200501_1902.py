# Generated by Django 3.0.5 on 2020-05-01 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_settings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercise',
            old_name='instructions',
            new_name='instructions_url',
        ),
        migrations.RenameField(
            model_name='exercise',
            old_name='exercise_repo',
            new_name='repo_url',
        ),
    ]
