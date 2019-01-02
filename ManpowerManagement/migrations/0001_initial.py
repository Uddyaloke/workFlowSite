# Generated by Django 2.1.4 on 2019-01-02 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import river.models.fields.state


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('role', '0001_initial'),
        ('river', '0010_auto_20190103_0030'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField(verbose_name='Employee ID')),
                ('emp_name', models.CharField(max_length=20, verbose_name='Name')),
                ('emp_desig', models.CharField(max_length=10, verbose_name='Designation')),
                ('country', models.CharField(max_length=30, verbose_name='Country')),
                ('branch', models.CharField(max_length=30, verbose_name='Branch')),
                ('office_location', models.CharField(max_length=30, verbose_name='Office Location')),
                ('contact_no', models.CharField(max_length=15, verbose_name='Contact No')),
                ('skill_set', models.CharField(max_length=50, verbose_name='Skill Set')),
                ('exp_yrs', models.IntegerField(verbose_name='Experience (Years)')),
                ('creator_comments_history', models.CharField(blank=True, max_length=600, null=True, verbose_name='Record Creator Comments History')),
                ('add_creator_comments', models.CharField(blank=True, max_length=200, null=True, verbose_name='Add Comments for Record Creator')),
                ('approver_comments_history', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Record Approver Comments History')),
                ('add_approver_comments', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Add Comments for Record Approver')),
                ('account_manager', models.CharField(blank=True, editable=False, max_length=20, null=True, verbose_name='Account Manager')),
                ('onboard_date', models.DateField(blank=True, null=True, verbose_name='Onboard Date')),
                ('cswon', models.CharField(blank=True, max_length=20, null=True, verbose_name='CSWON')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified Date')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='create_by', to=settings.AUTH_USER_MODEL)),
                ('status', river.models.fields.state.StateField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='river.State')),
                ('supervisor', models.ForeignKey(blank=True, limit_choices_to=models.Q(('primary_role', 'PL'), ('primary_role', 'AM'), ('secondary_role', 'PL'), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='role.Role')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='update_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
