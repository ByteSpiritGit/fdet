# Generated by Django 4.1.6 on 2023-04-14 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0005_evaluation_block_evaluation_evaluation_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='evaluation_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluations.evaluation_block'),
        ),
    ]