# Generated by Django 3.2.21 on 2023-10-03 21:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vdiApp', '0003_template_custom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='custom_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
