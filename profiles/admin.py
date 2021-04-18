from django.contrib import admin

from .models import Mentor, Profile, Student, User

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Mentor)
admin.site.register(Student)
