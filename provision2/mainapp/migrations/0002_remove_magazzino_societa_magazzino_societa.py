# Generated by Django 5.0.6 on 2024-08-07 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='magazzino',
            name='societa',
        ),
        migrations.AddField(
            model_name='magazzino',
            name='societa',
            field=models.ManyToManyField(to='mainapp.societa'),
        ),
    ]
