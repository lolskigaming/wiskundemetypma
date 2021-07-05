# Generated by Django 3.1.5 on 2021-07-03 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oefenen', '0003_auto_20210703_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='onderwerp',
            old_name='onderwerp',
            new_name='naam',
        ),
        migrations.RenameField(
            model_name='vaardigheid',
            old_name='onderwerp',
            new_name='bijbehorend_onderwerp',
        ),
        migrations.RenameField(
            model_name='vaardigheid',
            old_name='vaardigheid',
            new_name='naam',
        ),
        migrations.AddField(
            model_name='onderwerp',
            name='start',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='oefenen.vaardigheid'),
        ),
    ]
