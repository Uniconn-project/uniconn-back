# Generated by Django 3.2 on 2021-07-25 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0016_auto_20210709_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='university',
            name='is_active',
        ),
    ]
