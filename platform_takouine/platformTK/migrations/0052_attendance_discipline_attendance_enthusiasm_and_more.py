# Generated by Django 5.1 on 2024-10-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0051_schedule_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='discipline',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='enthusiasm',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
        migrations.AddField(
            model_name='attendance',
            name='seriousness',
            field=models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True),
        ),
    ]
