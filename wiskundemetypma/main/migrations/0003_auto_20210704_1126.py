# Generated by Django 3.2.5 on 2021-07-04 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_usersettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='user',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='usersettings',
        ),
    ]