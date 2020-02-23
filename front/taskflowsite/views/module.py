# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views import View
from django.http import HttpResponse
from taskflowsite.models import Modules


class ModuleListView(View):
    def get(self, request):
        context = {}
        modules = Modules.objects.all()
        context["modules"] = modules
        return render(request, "module_list.html", context)


class ModuleSaveView(View):
    def get(self, request):
        return render(request, "module_save.html")


def module_delete(request):
    return HttpResponse("ok")
