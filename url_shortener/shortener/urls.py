from django.urls import path

from . import views

app_name = 'shortener'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<str:shorturl>/stats', views.stats, name='stats'),
    path('<str:shorturl>', views.goto, name='goto'),
]
