# Generated by Django 4.0.2 on 2022-02-15 21:00
# Generated by Django 4.0.2 on 2022-02-15 21:25
# Generated by Django 4.0.2 on 2022-02-15 21:15
<<<<<<< HEAD
# Generated by Django 4.0.2 on 2022-02-15 21:00
# Generated by Django 4.0.2 on 2022-02-15 21:25
=======
>>>>>>> a570e2a4daf6074eeda790f120897933f92630f6

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rareapi', '0003_remove_subscription_ended_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='rareuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='rareapi.Subscription', to='rareapi.RareUser'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='tags', through='rareapi.PostTag', to='rareapi.Tag'),
        ),
    ]
