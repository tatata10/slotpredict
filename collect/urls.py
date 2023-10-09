# -*- coding: utf-8 -*-
#from django.urls import path
from . import views
from django.urls import path, include, re_path
from django.contrib import admin
from .analytics import analytics

urlpatterns = [
             path('',views.index,name='index'),
             path('form',views.form,name='form'),
             #path('excel',views.form,name='excel'),
             path('admin/', admin.site.urls),
             re_path(r'mplimage.png', analytics.regression_analysis),
             ]
