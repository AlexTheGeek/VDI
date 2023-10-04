# Generated by Django 4.2.5 on 2023-10-04 08:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('custom_id', models.CharField(default='f49dbca6-19a5-402c-9b38-9d4113393f71', editable=False, max_length=36, unique=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('custom_id', models.CharField(default='01c08741-5366-466b-a45c-faf77300eaa2', editable=False, max_length=36, unique=True)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('custom_id', models.CharField(default='6dee4491-2efa-43cf-9544-905857c4e967', editable=False, max_length=36, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('last_interaction', models.DateTimeField(auto_now=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vdiApp.template')),
            ],
        ),
    ]
