from django.contrib import admin

from .models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Link,
    Market,
    Project,
    ProjectEnteringRequest,
    ProjectStar,
)

admin.site.register(Market)
admin.site.register(Link)
admin.site.register(Project)
admin.site.register(ProjectStar)
admin.site.register(ProjectEnteringRequest)
admin.site.register(Discussion)
admin.site.register(DiscussionStar)
admin.site.register(DiscussionReply)
