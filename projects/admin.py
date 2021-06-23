from django.contrib import admin

from .models import Link, Market, Project, ProjectEnteringRequest

admin.site.register(Market)
admin.site.register(Link)
admin.site.register(Project)
admin.site.register(ProjectEnteringRequest)
