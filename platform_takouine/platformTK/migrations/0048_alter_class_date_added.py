# Generated by Django 5.1 on 2024-09-25 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0047_alter_class_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='date_added',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
