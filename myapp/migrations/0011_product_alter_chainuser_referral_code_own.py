# Generated by Django 4.1.7 on 2023-12-06 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_remove_chainuser_referrer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(max_length=5, unique=True)),
                ('p_title', models.CharField(max_length=255)),
                ('p_stocked', models.BooleanField(default=True)),
                ('p_description', models.TextField()),
                ('p_img', models.ImageField(blank=True, null=True, upload_to='product_images/')),
            ],
        ),
        migrations.AlterField(
            model_name='chainuser',
            name='referral_code_own',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
