# Generated by Django 5.0.6 on 2024-05-29 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptop', '0002_rename_telefon_laptop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
    ]
