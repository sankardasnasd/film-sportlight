# Generated by Django 4.2.5 on 2023-09-27 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_movie_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='theate_promotion',
            name='filename',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
