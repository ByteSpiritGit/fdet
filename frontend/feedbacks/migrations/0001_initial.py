# Generated by Django 4.1.6 on 2023-05-06 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evaluations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation_Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.BooleanField()),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluations.evaluation_block')),
            ],
        ),
    ]
