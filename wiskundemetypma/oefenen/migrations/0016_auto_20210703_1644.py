# Generated by Django 3.1.5 on 2021-07-03 14:44

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oefenen', '0015_auto_20210703_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaardigheid',
            name='kennis',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, max_length=200, null=True, verbose_name='self'),
        ),
        migrations.DeleteModel(
            name='Voorkennis',
        ),
    ]
