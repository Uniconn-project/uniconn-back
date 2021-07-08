from django.contrib import admin

from .models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Link,
    Market,
    Project,
    ProjectEnteringRequest,
)

admin.site.register(Market)
admin.site.register(Link)
admin.site.register(Project)
admin.site.register(ProjectEnteringRequest)
admin.site.register(Discussion)
admin.site.register(DiscussionStar)
admin.site.register(DiscussionReply)
