# Generated by Django 3.2 on 2021-06-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0021_link_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(default='{"blocks": [{"key": "5v3ub", "text": "Sem descrição...", "type": "unstyled", "depth": 0, "inlineStyleRanges": [], "entityRanges": [], "data": {}}], "entityMap": {}}', help_text='Detailed description', max_length=20000),
        ),
    ]
