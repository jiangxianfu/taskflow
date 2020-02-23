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
from taskflowsite.views.flow import FlowListView, FlowSaveView, flow_delete
from taskflowsite.views.instance import InstanceListView, InstanceSaveView, instance_delete
from taskflowsite.views.instance_step import InstanceStepsView
from taskflowsite.views.flow_step import FlowStepsView

urlpatterns = [
    # index
    path('', IndexView.as_view(), name='index'),
    # module
    path('module/list/', ModuleListView.as_view(), name='module_list'),
    path('module/save/<int:id>/', ModuleSaveView.as_view(), name='module_save'),
    path('module/delete/<int:id>/', module_delete, name='module_delete'),
    # flow
    path('flow/list/', FlowListView.as_view(), name='flow_list'),
    path('flow/save/<int:id>/', FlowSaveView.as_view(), name='flow_save'),
    path('flow/delete/<int:id>/', flow_delete, name='flow_delete'),

    path('flow/steps/<int:flow_id>/', FlowStepsView.as_view(), name="flow_steps"),
    # instance
    path('instance/list/', InstanceListView.as_view(), name='instance_list'),
    path('instance/save/<int:id>/', InstanceSaveView.as_view(), name='instance_save'),
    path('instance/delete/<int:id>/', instance_delete, name='instance_delete'),

    path('instance/steps/<int:instance_id>/', InstanceStepsView.as_view(), name="instance_steps"),
    # admin urls
    path('admin/', admin.site.urls)
]
