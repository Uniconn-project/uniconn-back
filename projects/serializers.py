from profiles.serializers import ProfileSerializer02, ProfileSerializer03
from rest_framework import serializers

from .models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Field,
    Link,
    Project,
    ProjectMember,
    ProjectRequest,
    Tool,
    ToolCategory,
)


class FieldSerializer01(serializers.ModelSerializer):
    """
    Field serializer that serializes only the *id* and *name* of a given field object.
    """

    class Meta:
        model = Field
        fields = ["id", "name"]


class LinkSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "name", "href"]


class ToolSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ["id", "name", "href"]


class ToolCategorySerializer01(serializers.ModelSerializer):
    tools = ToolSerializer01(many=True)

    class Meta:
        model = ToolCategory
        fields = ["id", "name", "tools"]


class ProjectStarSerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer03()

    class Meta:
        model = DiscussionStar
        fields = ["id", "profile"]


class ProjectMemberSerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer03()
    role = serializers.DictField(source="role_value_and_readable")

    class Meta:
        model = ProjectMember
        fields = ["id", "profile", "role"]


class ProjectSerializer01(serializers.ModelSerializer):
    """
    Light project serializer - useful for projects list items
    """

    category = serializers.DictField(source="category_value_and_readable")
    members_profiles = ProfileSerializer02(many=True)
    fields = FieldSerializer01(many=True)
    stars = ProjectStarSerializer01(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "category",
            "name",
            "slogan",
            "image",
            "members_profiles",
            "fields",
            "stars",
            "discussions_length",
        ]


class ProjectSerializer02(serializers.ModelSerializer):
    """
    Heavy project serializer - useful for project page
    """

    category = serializers.DictField(source="category_value_and_readable")
    members = ProjectMemberSerializer01(many=True)
    pending_invited_profiles = ProfileSerializer03(many=True)
    fields = FieldSerializer01(many=True)
    links = LinkSerializer01(many=True)
    tools_categories = ToolCategorySerializer01(many=True)
    stars = ProjectStarSerializer01(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "category",
            "name",
            "slogan",
            "image",
            "description",
            "members",
            "pending_invited_profiles",
            "fields",
            "links",
            "tools_categories",
            "stars",
            "discussions_length",
        ]


class ProjectSerializer03(serializers.ModelSerializer):
    """
    Lightest project serializer - only id, name and image
    """

    class Meta:
        model = Project
        fields = ["id", "name", "image"]


class ProjectRequestSerializer01(serializers.ModelSerializer):
    project = ProjectSerializer03()
    profile = ProfileSerializer02()

    class Meta:
        model = ProjectRequest
        fields = ["id", "message", "project", "profile"]


class DiscussionStarSerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer03()

    class Meta:
        model = DiscussionStar
        fields = ["id", "profile"]


class DiscussionReplySerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer03()

    class Meta:
        model = DiscussionReply
        fields = ["id", "profile", "content", "created_at"]


class DiscussionSerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer03()
    category = serializers.DictField(source="category_value_and_readable")
    stars = DiscussionStarSerializer01(many=True)
    replies = DiscussionReplySerializer01(many=True)

    class Meta:
        model = Discussion
        fields = ["id", "title", "body", "category", "profile", "stars", "replies", "created_at"]


class DiscussionSerializer02(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source="project.id")

    class Meta:
        model = Discussion
        fields = ["id", "title", "project_id"]


class DiscussionStarSerializer02(serializers.ModelSerializer):
    profile = ProfileSerializer02()
    discussion = DiscussionSerializer02()

    class Meta:
        model = DiscussionStar
        fields = ["id", "profile", "discussion", "created_at"]


class DiscussionReplySerializer02(serializers.ModelSerializer):
    profile = ProfileSerializer02()
    discussion = DiscussionSerializer02()

    class Meta:
        model = DiscussionReply
        fields = ["id", "profile", "discussion", "content", "created_at"]
