# Generated by Django 5.1 on 2024-09-19 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0036_alter_prof_date_de_naissance_alter_prof_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
