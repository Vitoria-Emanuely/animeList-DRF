# Generated by Django 3.2.8 on 2021-11-12 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='titulo',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
