# Generated by Django 3.1.5 on 2021-01-16 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=256)),
                ('sesh_date', models.DateTimeField(verbose_name='Session Date')),
                ('score', models.FloatField(default=0.0)),
            ],
        ),
    ]
