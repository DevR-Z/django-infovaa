# Generated by Django 5.1.1 on 2024-09-25 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infovanaDB', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titulo',
            name='year',
            field=models.CharField(max_length=20),
        ),
    ]
