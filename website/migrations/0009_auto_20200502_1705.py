# Generated by Django 3.0.5 on 2020-05-02 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20200502_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
