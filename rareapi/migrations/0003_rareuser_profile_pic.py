# Generated by Django 4.0.2 on 2022-02-17 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0002_reaction_postreaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='rareuser',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='profilepics'),
        ),
    ]
