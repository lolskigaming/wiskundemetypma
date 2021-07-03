# Generated by Django 3.1.5 on 2021-07-03 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oefenen', '0018_auto_20210703_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaardigheid',
            name='volgende',
            field=models.ManyToManyField(related_name='vaardigheid_volgende', to='oefenen.Vaardigheid'),
        ),
        migrations.AlterField(
            model_name='vaardigheid',
            name='voorkennis',
            field=models.ManyToManyField(related_name='vaardigheid_voorkennis', to='oefenen.Vaardigheid'),
        ),
    ]
