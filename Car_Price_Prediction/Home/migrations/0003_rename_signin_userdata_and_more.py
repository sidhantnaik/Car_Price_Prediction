# Generated by Django 5.1.2 on 2024-12-06 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_signin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Signin',
            new_name='UserData',
        ),
        migrations.RenameField(
            model_name='userdata',
            old_name='passw',
            new_name='password',
        ),
    ]
