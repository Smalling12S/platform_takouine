# Generated by Django 5.1 on 2024-09-23 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0042_class_date_added_alter_class_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='date_added',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]