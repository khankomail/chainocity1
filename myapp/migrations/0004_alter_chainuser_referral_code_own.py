# Generated by Django 4.1.7 on 2023-12-05 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_chainuser_referral_code_users_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chainuser',
            name='referral_code_own',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
