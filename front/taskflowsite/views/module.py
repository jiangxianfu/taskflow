
# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views import View
from django.http import HttpResponse

class ModuleListView(View):
    def get(self, request):
        return render(request, "index.html")

class ModuleSaveView(View):
    def get(self, request):
        return render(request, "index.html")

def module_delete(request):
    return HttpResponse("ok")
