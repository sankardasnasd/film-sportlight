# Generated by Django 3.0 on 2023-09-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theatre',
            name='status',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
