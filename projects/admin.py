from django.contrib import admin

from .models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Field,
    Link,
    Project,
    ProjectMember,
    ProjectRequest,
    ProjectStar,
    Tool,
    ToolCategory,
)

admin.site.register(Field)
admin.site.register(Link)
admin.site.register(ToolCategory)
admin.site.register(Tool)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectStar)
admin.site.register(ProjectRequest)
admin.site.register(Discussion)
admin.site.register(DiscussionStar)
admin.site.register(DiscussionReply)
