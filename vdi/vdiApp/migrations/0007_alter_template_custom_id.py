# Generated by Django 3.2.21 on 2023-10-03 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vdiApp', '0006_alter_template_custom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='custom_id',
            field=models.CharField(editable=False, max_length=36, unique=True),
        ),
    ]
