from django.urls import path, include

from . import views

from django.contrib.auth.decorators import login_required
from django.contrib import admin

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('social_django.urls')),
    path('profile/', views.profile),
    path('task1/', views.task1),
    path('task2/', views.task2),
    path('task3/', views.task3),
    path('task4/', views.task4),
    path('task5/', views.task5),
    path('task6/', views.task6),
    path('task7/', views.task7),
    path('task8/', views.task8),
    path('logout/', views.logout),
]
