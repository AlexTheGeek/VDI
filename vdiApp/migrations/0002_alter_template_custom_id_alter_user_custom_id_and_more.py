# Generated by Django 4.2.5 on 2023-10-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdiApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='custom_id',
            field=models.CharField(default='8e4be5f7-de09-444d-85cd-70f82be0f565', editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='custom_id',
            field=models.CharField(default='5af40b16-3ae5-425e-ae9a-890793ef24f8', editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='vm',
            name='custom_id',
            field=models.CharField(default='951c9003-6be5-4b20-913a-e8a74a6b69b8', editable=False, max_length=36, unique=True),
        ),
    ]
