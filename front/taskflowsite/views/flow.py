# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views import View
from django.http import HttpResponse
from taskflowsite.models import Flows


class FlowListView(View):
    def get(self, request):
        context = {}
        flows = Flows.objects.all()
        context["flows"] = flows
        return render(request, "flow_list.html", context)


class FlowSaveView(View):
    def get(self, request):
        return render(request, "flow_save.html")


def flow_delete(request):
    return HttpResponse("ok")
