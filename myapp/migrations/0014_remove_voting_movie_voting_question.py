# Generated by Django 4.2.5 on 2023-10-06 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voting',
            name='MOVIE',
        ),
        migrations.AddField(
            model_name='voting',
            name='QUESTION',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.question'),
        ),
    ]