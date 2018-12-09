# Generated by Django 2.1.4 on 2018-12-09 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eToolActivation', '0006_remove_etoolactivation_completion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='etoolactivation',
            name='spoc_comments',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='SPOC Comments'),
        ),
        migrations.AddField(
            model_name='etoolactivation',
            name='team_lead_comments',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Team Lead Comments'),
        ),
    ]