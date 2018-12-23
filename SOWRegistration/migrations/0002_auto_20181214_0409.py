# Generated by Django 2.1.4 on 2018-12-13 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SOWRegistration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sowregistration',
            name='amendment_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Amendment End Date'),
        ),
        migrations.AddField(
            model_name='sowregistration',
            name='amendment_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Amendment Start Date'),
        ),
        migrations.AddField(
            model_name='sowregistration',
            name='amendment_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Amendment Value'),
        ),
    ]
