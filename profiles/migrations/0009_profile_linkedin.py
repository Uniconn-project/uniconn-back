# Generated by Django 3.2 on 2021-05-18 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linkedIn',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
