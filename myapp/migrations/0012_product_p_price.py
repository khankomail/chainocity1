# Generated by Django 4.1.7 on 2023-12-06 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_product_alter_chainuser_referral_code_own'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='p_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
