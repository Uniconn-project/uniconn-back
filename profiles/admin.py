from django.contrib import admin

from .models import Mentor, Student, User

admin.site.register(User)
admin.site.register(Mentor)
admin.site.register(Student)
