# Generated by Django 3.0 on 2023-09-23 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_theatre_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie_review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('MOVIE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Movie')),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User')),
            ],
        ),
    ]