# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views import View
from taskflowsite.models import Flows
from taskflowsite.models import FlowSteps


class FlowStepsView(View):
    def get(self, request, flow_id):
        context = {}
        flow = Flows.objects.get(id=flow_id)
        flow_steps = FlowSteps.objects.filter(flowid=flow_id)
        context["flow_steps"] = flow_steps
        context["flow"] = flow
        # print(flow_steps)
        return render(request, "flow_steps.html", context)
