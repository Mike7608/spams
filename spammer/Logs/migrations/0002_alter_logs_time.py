# Generated by Django 4.2.1 on 2024-01-30 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время последней попытки'),
        ),
    ]
