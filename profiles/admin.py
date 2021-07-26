from django.contrib import admin

from .models import Profile, Skill, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Skill)
