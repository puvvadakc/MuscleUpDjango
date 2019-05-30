# Generated by Django 2.2 on 2019-05-30 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190528_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programs',
            name='fitness_goal',
            field=models.CharField(choices=[('BB', 'BodyBuilding (Weight Gain)'), ('ST', 'Strength Training'), ('CA', 'Cardio (Endurance)'), ('WL', 'Weight Loss (Fat Reduction)')], max_length=2),
        ),
    ]
