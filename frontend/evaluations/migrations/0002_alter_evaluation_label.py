# Generated by Django 4.1.6 on 2023-03-28 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='label',
            field=models.CharField(max_length=100),
        ),
    ]
