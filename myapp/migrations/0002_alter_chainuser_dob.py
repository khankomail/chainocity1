# Generated by Django 4.1.7 on 2023-12-04 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chainuser',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
    ]
