# Generated by Django 2.1.4 on 2018-12-09 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empMaster', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empmaster',
            name='etool_activation',
        ),
    ]
