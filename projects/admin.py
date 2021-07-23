from django.contrib import admin
from profiles.models import StudentSkill

from .models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Link,
    Market,
    Project,
    ProjectEnteringRequest,
    ProjectStar,
    Tool,
    ToolCategory,
)

admin.site.register(Market)
admin.site.register(Link)
admin.site.register(ToolCategory)
admin.site.register(Tool)
admin.site.register(Project)
admin.site.register(ProjectStar)
admin.site.register(ProjectEnteringRequest)
admin.site.register(Discussion)
admin.site.register(DiscussionStar)
admin.site.register(DiscussionReply)
admin.site.register(StudentSkill)
