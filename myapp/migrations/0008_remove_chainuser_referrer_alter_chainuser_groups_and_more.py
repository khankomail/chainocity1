# Generated by Django 4.1.7 on 2023-12-06 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0007_chainuser_referrer_alter_chainuser_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chainuser',
            name='referrer',
        ),
        migrations.AlterField(
            model_name='chainuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='chainuser_set', related_query_name='chainuser', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='chainuser',
            name='referral_code_other',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='chainuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='chainuser_set', related_query_name='chainuser', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
