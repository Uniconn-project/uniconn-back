# Generated by Django 3.2 on 2021-07-02 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20210624_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='Sem bio...', max_length=150, null=True),
        ),
    ]
