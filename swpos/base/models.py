# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class HiringDetails(models.Model):
    position = models.OneToOneField('Position', models.DO_NOTHING, primary_key=True)
    office_name = models.CharField(max_length=40, blank=True, null=True)
    hiring_number = models.IntegerField(blank=True, null=True)
    working_hours = models.CharField(max_length=20, blank=True, null=True)
    hourly_wage = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hiring_details'


class Position(models.Model):
    position_id = models.IntegerField(primary_key=True)  # The composite primary key (position_id, supervisor_id) found, that is not supported. The first column is selected.
    position_name = models.CharField(max_length=50)
    position_type = models.CharField(max_length=20, blank=True, null=True)
    supervisor = models.ForeignKey('Supervisor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'position'
        unique_together = (('position_id', 'supervisor'),)


class PositionDetail(models.Model):
    position = models.OneToOneField(Position, models.DO_NOTHING, primary_key=True)
    position_description = models.TextField()
    description_link = models.CharField(max_length=255, blank=True, null=True)
    requirements = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'position_detail'


class PositionTimeline(models.Model):
    position = models.OneToOneField(Position, models.DO_NOTHING, primary_key=True)
    application_deadline = models.DateField(blank=True, null=True)
    date_of_posting = models.DateField(blank=True, null=True)
    status_position = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'position_timeline'


class Supervisor(models.Model):
    supervisor_id = models.IntegerField(primary_key=True)
    professor_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'supervisor'
