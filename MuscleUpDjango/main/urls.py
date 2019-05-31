from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('programs', views.programs, name = 'programs'),
    path('programs/<int:program_id>', views.specificProgram, name='specificProgram'),
    path('progress', views.allProgress, name="allProgress"),
    path('progress/<int:program_id>', views.programProgress, name="programProgress"),
    path('recommended/<int:fitness_goal>', views.recommendedPrograms, name="recommendedPrograms"),
]