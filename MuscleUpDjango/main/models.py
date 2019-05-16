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
