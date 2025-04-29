from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_load, name='blog_load'),
]
