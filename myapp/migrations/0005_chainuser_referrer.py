# Generated by Django 4.1.7 on 2023-12-05 23:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_chainuser_referral_code_own'),
    ]

    operations = [
        migrations.AddField(
            model_name='chainuser',
            name='referrer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referred_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
