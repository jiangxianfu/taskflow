# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views import View
from django.http import HttpResponse
from taskflowsite.models import Instances


class InstanceListView(View):
    def get(self, request):
        context = {}
        instances = Instances.objects.all()
        context["instances"] = instances
        return render(request, "instance_list.html", context)


class InstanceSaveView(View):
    def get(self, request):
        return render(request, "instance_save.html")


def instance_delete(request):
    return HttpResponse("ok")
