# Generated by Django 5.1 on 2024-10-11 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0061_absencevalidationhistory_delete_attendancevalidation'),
    ]

    operations = [
        migrations.AddField(
            model_name='absencevalidationhistory',
            name='is_attendance',
            field=models.BooleanField(default=False),
        ),
    ]