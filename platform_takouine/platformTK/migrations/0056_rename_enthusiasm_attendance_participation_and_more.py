# Generated by Django 5.1 on 2024-10-09 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0055_parents_etudiants'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendance',
            old_name='enthusiasm',
            new_name='participation',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='seriousness',
        ),
    ]
