# Generated by Django 2.2.4 on 2019-08-23 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vue_plugins', '0009_vueplugin_repo_readme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vueplugin',
            name='repo_readme',
            field=models.URLField(blank=True, max_length=131072),
        ),
    ]
