# Generated by Django 2.1.4 on 2018-12-10 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eToolActivation', '0007_auto_20181210_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etoolactivation',
            name='emp_master',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_id', to='empMaster.empMaster'),
        ),
    ]