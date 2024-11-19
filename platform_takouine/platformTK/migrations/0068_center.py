# Generated by Django 5.1 on 2024-11-11 12:32

import platformTK.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0067_groups_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('code', models.CharField(blank=True, default=platformTK.models.generate_center_code, max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
    ]