# Generated by Django 5.0.6 on 2024-05-27 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telefon', '0003_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='telefon',
            name='price',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
    ]
