from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'auth'
urlpatterns = [
    path('signin', views.signin, name = 'signin'),
    path('signout', views.signout, name = 'signout'),
    path('register', views.register, name = 'register'),
    path('update', views.update, name = 'update'),
    path('delete', views.delete, name = 'delete')
]