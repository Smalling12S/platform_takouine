# Generated by Django 5.1 on 2024-08-27 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0010_competitions_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitions',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
