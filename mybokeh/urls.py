from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from .views import view_bk

app_name ='mybokeh'
urlpatterns = [
	path('',view_bk,name='mybokeh-plot'),
]