# Generated by Django 2.1.4 on 2018-12-22 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workList', '0002_worklist_mod_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklist',
            name='mod_url',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
