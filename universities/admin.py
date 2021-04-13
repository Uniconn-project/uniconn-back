from django.contrib import admin

from .models import Major, MajorField, University

admin.site.register(Major)
admin.site.register(MajorField)
admin.site.register(University)
