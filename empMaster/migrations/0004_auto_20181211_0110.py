# Generated by Django 2.1.4 on 2018-12-10 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('empMaster', '0003_empmaster_etoolactivation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empmaster',
            name='etoolactivation',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='eTool', to='eToolActivation.eToolActivation'),
        ),
    ]