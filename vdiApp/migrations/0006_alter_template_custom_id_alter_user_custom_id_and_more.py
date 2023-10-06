# Generated by Django 4.2.5 on 2023-10-04 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdiApp', '0005_alter_template_custom_id_alter_user_custom_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='custom_id',
            field=models.CharField(default='1d7bde8d-294b-48ee-be43-45dfb3cbac9d', editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='custom_id',
            field=models.CharField(default='40a060d3-85f9-486c-8371-565fef87f56c', editable=False, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='vm',
            name='custom_id',
            field=models.CharField(default='22f4e759-16df-4a52-a4fe-614f7b852a37', editable=False, max_length=36, unique=True),
        ),
    ]
