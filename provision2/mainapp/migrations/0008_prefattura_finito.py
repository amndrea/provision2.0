# Generated by Django 5.0.6 on 2024-08-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_prefattura_data_modifica'),
    ]

    operations = [
        migrations.AddField(
            model_name='prefattura',
            name='finito',
            field=models.BooleanField(default=False),
        ),
    ]
