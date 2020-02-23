# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views import View
from taskflowsite.models import InstanceSteps
from taskflowsite.models import Instances


class InstanceStepsView(View):
    def get(self, request, instance_id):
        context = {}
        instance = Instances.objects.get(id=instance_id)
        instance_steps = InstanceSteps.objects.filter(instanceid=instance_id)
        context["instance_steps"] = instance_steps
        context["instance"] = instance
        # print(instance_steps)
        return render(request, "instance_steps.html", context)
