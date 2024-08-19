# Generated by Django 5.1 on 2024-08-12 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platformTK', '0002_etudiant_etudiantcode_alter_etudiant_slugetudiant_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code_group', models.CharField(blank=True, editable=False, max_length=100, unique=True)),
                ('etudiants', models.ManyToManyField(related_name='groups', to='platformTK.etudiant')),
                ('profs', models.ManyToManyField(related_name='groups', to='platformTK.prof')),
            ],
        ),
    ]