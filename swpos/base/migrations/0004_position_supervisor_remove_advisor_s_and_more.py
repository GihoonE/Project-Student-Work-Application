# Generated by Django 4.2.7 on 2023-11-21 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0003_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Position",
            fields=[
                ("position_id", models.IntegerField(primary_key=True, serialize=False)),
                ("position_name", models.CharField(max_length=50)),
                (
                    "position_type",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
            ],
            options={
                "db_table": "position",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Supervisor",
            fields=[
                (
                    "supervisor_id",
                    models.IntegerField(primary_key=True, serialize=False),
                ),
                (
                    "professor_name",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
            ],
            options={
                "db_table": "supervisor",
                "managed": False,
            },
        ),
        migrations.RemoveField(
            model_name="advisor",
            name="s",
        ),
        migrations.DeleteModel(
            name="AuthGroup",
        ),
        migrations.DeleteModel(
            name="AuthGroupPermissions",
        ),
        migrations.DeleteModel(
            name="AuthPermission",
        ),
        migrations.DeleteModel(
            name="AuthUser",
        ),
        migrations.DeleteModel(
            name="AuthUserGroups",
        ),
        migrations.DeleteModel(
            name="AuthUserUserPermissions",
        ),
        migrations.DeleteModel(
            name="Classroom",
        ),
        migrations.DeleteModel(
            name="Department",
        ),
        migrations.DeleteModel(
            name="DjangoAdminLog",
        ),
        migrations.DeleteModel(
            name="DjangoContentType",
        ),
        migrations.DeleteModel(
            name="DjangoMigrations",
        ),
        migrations.DeleteModel(
            name="DjangoSession",
        ),
        migrations.RemoveField(
            model_name="prereq",
            name="course",
        ),
        migrations.RemoveField(
            model_name="section",
            name="course",
        ),
        migrations.RemoveField(
            model_name="takes",
            name="id",
        ),
        migrations.RemoveField(
            model_name="teaches",
            name="id",
        ),
        migrations.DeleteModel(
            name="TimeSlot",
        ),
        migrations.CreateModel(
            name="HiringDetails",
            fields=[
                (
                    "position",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="base.position",
                    ),
                ),
                ("office_name", models.CharField(blank=True, max_length=40, null=True)),
                ("hiring_number", models.IntegerField(blank=True, null=True)),
                (
                    "working_hours",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("hourly_wage", models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                "db_table": "hiring_details",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PositionDetail",
            fields=[
                (
                    "position",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="base.position",
                    ),
                ),
                ("position_description", models.TextField()),
                (
                    "description_link",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "requirements",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
            ],
            options={
                "db_table": "position_detail",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PositionTimeline",
            fields=[
                (
                    "position",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="base.position",
                    ),
                ),
                ("application_deadline", models.DateField(blank=True, null=True)),
                ("date_of_posting", models.DateField(blank=True, null=True)),
                (
                    "status_position",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
            ],
            options={
                "db_table": "position_timeline",
                "managed": False,
            },
        ),
        migrations.DeleteModel(
            name="Advisor",
        ),
        migrations.DeleteModel(
            name="Course",
        ),
        migrations.DeleteModel(
            name="Instructor",
        ),
        migrations.DeleteModel(
            name="Prereq",
        ),
        migrations.DeleteModel(
            name="Section",
        ),
        migrations.DeleteModel(
            name="Student",
        ),
        migrations.DeleteModel(
            name="Takes",
        ),
        migrations.DeleteModel(
            name="Teaches",
        ),
    ]
