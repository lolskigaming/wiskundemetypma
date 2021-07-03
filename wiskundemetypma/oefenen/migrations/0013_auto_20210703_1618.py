# Generated by Django 3.1.5 on 2021-07-03 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oefenen', '0012_auto_20210703_1604'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vaardigheid',
            options={'ordering': ['bijbehorend_onderwerp', 'nummer']},
        ),
        migrations.AddField(
            model_name='onderwerp',
            name='letter',
            field=models.CharField(default='A', max_length=4),
        ),
        migrations.AlterField(
            model_name='vaardigheid',
            name='nummer',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
