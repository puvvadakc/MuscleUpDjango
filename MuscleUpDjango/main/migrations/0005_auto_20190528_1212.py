# Generated by Django 2.2 on 2019-05-28 19:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190528_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='gender',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='progress',
            name='age',
            field=models.PositiveSmallIntegerField(default=20, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(130)]),
            preserve_default=False,
        ),
    ]
