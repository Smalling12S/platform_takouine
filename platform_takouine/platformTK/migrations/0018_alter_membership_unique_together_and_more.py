# Generated by Django 5.1 on 2024-09-04 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0017_membership'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='membership',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platformTK.groups'),
        ),
    ]
