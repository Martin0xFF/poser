# Generated by Django 3.1.5 on 2021-01-17 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_session_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='sesh_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Session Date'),
        ),
    ]
