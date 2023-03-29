# Generated by Django 4.1.6 on 2023-03-28 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('claim', models.CharField(max_length=1000)),
                ('label', models.IntegerField()),
                ('supports', models.FloatField()),
                ('refutes', models.FloatField()),
                ('evidence', models.CharField(max_length=1000)),
            ],
        ),
    ]
