# Generated by Django 4.2 on 2023-04-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userExtensions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextension',
            name='profile_picture',
            field=models.ImageField(default='default_profile_picture.jpg', upload_to='./media/profile_pictures'),
        ),
    ]
