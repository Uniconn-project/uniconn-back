# Generated by Django 3.2 on 2021-07-26 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0048_auto_20210725_2102'),
        ('profiles', '0021_auto_20210725_2102'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mentor',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
