from django.contrib import admin
from assigner.models import (
    User,
    Project,
    Task,
    SubmittedTask,
)

# Register your models here.
admin.site.register([User, Project, Task, SubmittedTask])
