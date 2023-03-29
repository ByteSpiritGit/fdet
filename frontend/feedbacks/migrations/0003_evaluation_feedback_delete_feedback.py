# Generated by Django 4.1.6 on 2023-03-29 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluations', '0003_alter_evaluation_evidence'),
        ('feedbacks', '0002_alter_feedback_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation_Feedback',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.BooleanField()),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evaluations.evaluation')),
            ],
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]
