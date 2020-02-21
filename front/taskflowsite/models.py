# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class FlowSteps(models.Model):
    flowid = models.IntegerField()
    modulename = models.CharField(max_length=128)
    inputargalias = models.TextField()  # This field type is a guess.
    outputargalias = models.TextField()  # This field type is a guess.
    stepnum = models.IntegerField()
    stepname = models.CharField(max_length=45)
    stepdescription = models.CharField(max_length=255)
    failed_retrycounts = models.IntegerField()
    nextstep_waitseconds = models.IntegerField()
    creator = models.CharField(max_length=45)
    createdtime = models.DateTimeField()
    updator = models.CharField(max_length=45)
    modifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'flow_steps'
        unique_together = (('flowid', 'stepnum'),)


class Flows(models.Model):
    name = models.CharField(unique=True, max_length=45)
    description = models.CharField(max_length=255)
    entry_arguments = models.TextField()  # This field type is a guess.
    stepcount = models.IntegerField()
    creator = models.CharField(max_length=45)
    createdtime = models.DateTimeField()
    updator = models.CharField(max_length=45)
    modifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'flows'


class InstanceRundata(models.Model):
    instanceid = models.IntegerField()
    keyname = models.CharField(max_length=128)
    keyvalue = models.CharField(max_length=2000)
    keytype = models.CharField(max_length=45)
    createdtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instance_rundata'
        unique_together = (('instanceid', 'keyname'),)


class InstanceSteps(models.Model):
    instanceid = models.IntegerField(blank=True, null=True)
    stepnum = models.IntegerField(blank=True, null=True)
    stepname = models.CharField(max_length=128, blank=True, null=True)
    arguments = models.TextField(blank=True, null=True)  # This field type is a guess.
    status = models.CharField(max_length=10, blank=True, null=True)
    message = models.CharField(max_length=5000, blank=True, null=True)
    createdtime = models.DateTimeField(blank=True, null=True)
    modifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instance_steps'


class Instances(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=255)
    flowid = models.IntegerField()
    arguments = models.TextField()  # This field type is a guess.
    stepcount = models.IntegerField()
    curstepnum = models.IntegerField()
    curstepruncount = models.IntegerField()
    nextruntime = models.DateTimeField()
    status = models.CharField(max_length=10)
    creator = models.CharField(max_length=45)
    createdtime = models.DateTimeField()
    updator = models.CharField(max_length=45)
    modifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'instances'


class Modules(models.Model):
    name = models.CharField(unique=True, max_length=128)
    description = models.CharField(max_length=255)
    arguments = models.TextField()  # This field type is a guess.
    creator = models.CharField(max_length=45)
    createdtime = models.DateTimeField()
    updator = models.CharField(max_length=45)
    modifiedtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'modules'
