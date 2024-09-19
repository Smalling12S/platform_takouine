# Generated by Django 5.1 on 2024-09-19 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0037_alter_groups_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='commande',
            name='date_ordered',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='competitions',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='prof',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
