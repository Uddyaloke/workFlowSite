# Generated by Django 2.1.4 on 2019-01-02 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManpowerManagement', '0002_auto_20190103_0148'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empregistration',
            options={'verbose_name': 'Employee Registration', 'verbose_name_plural': 'Employee Registrations'},
        ),
        migrations.RemoveField(
            model_name='empregistration',
            name='add_creator_comments',
        ),
        migrations.RemoveField(
            model_name='empregistration',
            name='creator_comments_history',
        ),
        migrations.AddField(
            model_name='empregistration',
            name='add_status_change_comments',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Add Status Change Comments'),
        ),
        migrations.AddField(
            model_name='empregistration',
            name='status_change_comments_history',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Status Change Comments History'),
        ),
        migrations.AddField(
            model_name='empregistration',
            name='status_change_date',
            field=models.DateField(blank=True, null=True, verbose_name='Status Change Date'),
        ),
        migrations.AddField(
            model_name='empregistration',
            name='status_change_history',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Status Change History'),
        ),
    ]
