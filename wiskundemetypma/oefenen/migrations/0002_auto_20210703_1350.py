# Generated by Django 3.1.5 on 2021-07-03 11:50

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('oefenen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaardigheid',
            name='voorkennis',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('a', 'Vergelijkingen'), ('b', 'Functies'), ('c', 'Rekenkundige regels'), ('d', 'Hellingen en de afgeleide'), ('e', 'Meetkunde')], max_length=9, null=True),
        ),
        migrations.CreateModel(
            name='Onderwerp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onderwerp', models.CharField(max_length=128)),
                ('start', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oefenen.vaardigheid')),
            ],
        ),
    ]
