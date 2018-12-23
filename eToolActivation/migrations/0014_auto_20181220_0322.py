# Generated by Django 2.1.4 on 2018-12-19 21:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0008_role_view_all'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eToolActivation', '0013_auto_20181219_0404'),
    ]

    operations = [
        migrations.AddField(
            model_name='etoolactivation',
            name='account_manager',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Account Manager'),
        ),
        migrations.AddField(
            model_name='etoolactivation',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='etool_create_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='etoolactivation',
            name='supervisor',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('primary_role', 'PL'), ('primary_role', 'AM'), ('secondary_role', 'PL'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='role.Role'),
        ),
        migrations.AddField(
            model_name='etoolactivation',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='etool_update_by', to=settings.AUTH_USER_MODEL),
        ),
    ]