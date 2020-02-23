# -*- coding: utf-8 -*-
"""taskflowsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from taskflowsite.views.index import IndexView
from taskflowsite.views.module import ModuleListView, ModuleSaveView, module_delete

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('module/list', ModuleListView.as_view(), name='module_list'),
    path('module/save/(?P<pk>[0-9]+)', ModuleSaveView.as_view(), name='module_save'),
    path('module/delete/(?P<pk>[0-9]+)', module_delete, name='module_delete'),
    path('admin/', admin.site.urls)
]
