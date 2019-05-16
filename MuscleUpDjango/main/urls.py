from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('programs', views.programs, name = 'programs'),
    path('programs/<int:program_id>', views.specificProgram, name='specificProgram')
]