# Generated by Django 4.2.5 on 2023-09-27 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_theate_promotion_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='theate_promotion',
            name='SHEDULE',
        ),
    ]
