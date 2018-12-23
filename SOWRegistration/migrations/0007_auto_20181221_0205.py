# Generated by Django 2.1.4 on 2018-12-20 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SOWRegistration', '0006_auto_20181218_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='sowregistration',
            name='account_manager',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Account Manager'),
        ),
        migrations.AddField(
            model_name='sowregistration',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sowreg_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sowregistration',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sowreg_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='woncreationextension',
            name='account_manager',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Account Manager'),
        ),
        migrations.AddField(
            model_name='woncreationextension',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='won_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='woncreationextension',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='won_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]