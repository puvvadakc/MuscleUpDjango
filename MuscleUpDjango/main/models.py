from django.db import models
from django.http import HttpResponse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    membership = models.CharField(max_length = 50, null = False, default = "normal")
    gender = models.CharField(max_length = 10, null = False)
    dob = models.DateField(null = False)
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)], null = False)
    def save(self, *args, **kwargs):
        if self.membership in ['administrator', 'member', 'normal'] and self.gender in ['male', 'female']:
            super().save(*args, **kwargs)
        else:
            return HttpResponse('This is not a valid membership', status = 400) 


class Programs(models.Model):
    name = models.CharField(max_length = 50, null = False)
    description = models.TextField(max_length = 5000, null = False)
    BODYBUILDING = 'BB'
    STRENGTH = 'ST'
    CARDIO = 'CA'
    WEIGHTLOSS = 'WL'
    FITNESS_GOAL_TYPE = (
        (BODYBUILDING, 'BodyBuilding (Weight Gain)'),
        (STRENGTH, 'Strength Training'),
        (CARDIO, 'Cardio (Endurance)'),
        (WEIGHTLOSS, 'Weight Loss (Fat Reduction)')
    )

    fitness_goal = models.CharField(max_length=1, choices=FITNESS_GOAL_TYPE, null = False)
    author = models.ForeignKey(Users, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)



class Progress(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    program = models.ForeignKey(Programs, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)
    height = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(120)], null = False)
    gender = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), 
        MaxValueValidator(1)], null = False)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(130)], null = False)
    barbell_row = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(1000)], null = True)
    bench_press = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(1500)], null = True)
    dead_lift = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(1500)], null = True)
    overhead_press = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(1000)], null = True)
    squat = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(1500)], null = True)
    dips_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(2000)], null = True)
    pullups_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(2000)], null = True)
    pushups_count = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(2000)], null = True)
    mile_time_sec = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(120), 
        MaxValueValidator(5000)], null = True)
    heartrate_bpm = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), 
        MaxValueValidator(250)], null = True)
    steps = models.PositiveIntegerField(
        validators=[MinValueValidator(1), 
        MaxValueValidator(100000)], null = True)
    weight = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(20), 
        MaxValueValidator(1000)], null = True)
    bodyfat_perc = models.DecimalField(max_digits=2, decimal_places=2, null=True)
