# Generated by Django 2.0 on 2019-05-28 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpsession',
            name='data',
        ),
    ]
