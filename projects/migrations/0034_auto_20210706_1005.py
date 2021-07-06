# Generated by Django 3.2 on 2021-07-06 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20210702_1503'),
        ('projects', '0033_alter_projectenteringrequest_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discussion',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='DiscussionStar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualized', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('discussion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='projects.discussion')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discussion_stars', to='profiles.profile')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
