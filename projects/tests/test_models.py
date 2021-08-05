import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from projects.models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Field,
    Link,
    Project,
    ProjectEntryRequest,
    ProjectInvitation,
    ProjectMember,
    ProjectStar,
    Tool,
    ToolCategory,
    discussion_categories_choices,
    project_categories_choices,
    project_member_role_choices,
)

User = get_user_model()


class TestField(TestCase):
    def test_create_delete(self):
        # test create
        field = Field.objects.create()
        self.assertIsInstance(field, Field)
        self.assertEqual(field.pk, 1)

        # test delete
        field.delete()
        self.assertFalse(Field.objects.exists())

    def test_fields(self):
        field = Field.objects.create()

        name = "Educação"
        field.name = name

        field.save()

        self.assertEqual(field.name, name)

        # testing name unique constrain
        with transaction.atomic():
            self.assertRaises(IntegrityError, Field.objects.create, name=name)

    def test_str(self):
        field = Field.objects.create(name="Inovação")
        self.assertEqual(str(field), field.name)


class TestProject(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        project = Project.objects.create()
        self.assertIsInstance(project, Project)
        self.assertEqual(project.pk, 1)
        self.assertEqual(
            project.description,
            '{"blocks": [{"key": "5v3ub", "text": "Sem descrição...", "type": "unstyled", "depth": 0, "inlineStyleRanges": [], "entityRanges": [], "data": {}}], "entityMap": {}}',
        )
        self.assertEqual(project.image, "default_project.jpg")
        self.assertLessEqual(now_aware, project.created_at)
        self.assertLessEqual(now_aware, project.updated_at)

        # test delete
        project.delete()
        self.assertFalse(Project.objects.exists())

    def test_fields(self):
        project = Project.objects.create()

        category = "startup"
        name = "4Share"
        slogan = "Awesome technologies 4 share"
        description = "Detailed description..."
        image = "4share_logo.jpeg"

        field01 = Field.objects.create(name="agriculture")
        field02 = Field.objects.create(name="computer-brain interface")
        project.fields.add(field01, field02)

        project.category = category
        project.name = name
        project.slogan = slogan
        project.description = description
        project.image = image
        project.save()

        self.assertEqual(project.category, category)
        self.assertEqual(project.name, name)
        self.assertEqual(project.slogan, slogan)
        self.assertEqual(project.description, description)
        self.assertEqual(project.image, image)

        self.assertEqual(list(project.fields.all()), [field01, field02])

    def test_related_name(self):
        project = Project.objects.create()

        # fields
        field = Field.objects.create()
        project.fields.add(field)
        project.save()
        self.assertIn(project, field.projects.all())

    def test_get_project_categories_choices_staticmethod(self):
        self.assertEqual(
            Project.get_project_categories_choices(),
            project_categories_choices,
        )

        self.assertEqual(
            Project.get_project_categories_choices(index=0),
            [project_category[0] for project_category in project_categories_choices],
        )

        self.assertEqual(
            Project.get_project_categories_choices(index=1),
            [project_category[1] for project_category in project_categories_choices],
        )

    def test_str(self):
        project = Project.objects.create(name="Uniconn")
        self.assertEqual(str(project), project.name)

    def test_members_profiles_method(self):
        project = Project.objects.create()

        profile01 = User.objects.create(username="peter").profile
        profile02 = User.objects.create(username="taylor").profile

        ProjectMember.objects.create(project=project, profile=profile01)
        ProjectMember.objects.create(project=project, profile=profile02)

        self.assertEqual(project.members_profiles, [profile01, profile02])

    def test_pending_invited_profiles_method(self):
        project = Project.objects.create()

        profile01 = User.objects.create(username="peter").profile
        profile02 = User.objects.create(username="taylor").profile

        ProjectInvitation.objects.create(project=project, receiver=profile01)
        ProjectInvitation.objects.create(project=project, receiver=profile02)

        self.assertEqual(project.pending_invited_profiles, [profile02, profile01])

    def test_category_value_and_readable_method(self):
        project = Project.objects.create(category=project_categories_choices[0][0])
        self.assertEqual(
            project.category_value_and_readable,
            {"value": project_categories_choices[0][0], "readable": project_categories_choices[0][1]},
        )

    def test_discussions_length_method(self):
        project = Project.objects.create()

        Discussion.objects.create(project=project)
        Discussion.objects.create(project=project)
        Discussion.objects.create(project=project)

        self.assertEqual(project.discussions_length, 3)


class TestProjectMember(TestCase):
    def test_create_delete(self):
        # test create
        project_member = ProjectMember.objects.create()
        self.assertIsInstance(project_member, ProjectMember)
        self.assertEqual(project_member.pk, 1)

        # test delete
        project_member.delete()
        self.assertFalse(ProjectMember.objects.exists())

    def test_fields(self):
        project_member = ProjectMember.objects.create()

        profile = User.objects.create().profile
        project = Project.objects.create()
        role = "admin"

        project_member.profile = profile
        project_member.project = project
        project_member.role = role

        project_member.save()

        self.assertEqual(project_member.profile, profile)
        self.assertEqual(project_member.project, project)
        self.assertEqual(project_member.role, role)

    def test_project_relation(self):
        project = Project.objects.create()
        project_member = ProjectMember.objects.create(project=project)

        # testing related name
        self.assertIn(project_member, project.members.all())

        # testing cascade
        project.delete()
        self.assertFalse(ProjectMember.objects.exists())

    def test_profile_relation(self):
        profile = User.objects.create().profile
        project_member = ProjectMember.objects.create(profile=profile)

        # testing related name
        self.assertIn(project_member, profile.project_memberships.all())

        # testing cascade
        profile.delete()
        self.assertFalse(ProjectMember.objects.exists())

    def test_str(self):
        project = Project.objects.create(name="Simulatomic")
        profile = User.objects.create(username="john_p").profile
        project_member = ProjectMember.objects.create(project=project, profile=profile)
        self.assertEqual(str(project_member), f"{profile} [{project_member.role}] - {project}")

    def test_role_value_and_readable_method(self):
        project_member = ProjectMember.objects.create(role=project_member_role_choices[0][0])
        self.assertEqual(
            project_member.role_value_and_readable,
            {"value": project_member_role_choices[0][0], "readable": project_member_role_choices[0][1]},
        )


class TestProjectEntryRequest(TestCase):
    def test_create_delete(self):
        # test create
        project_entry_request = ProjectEntryRequest.objects.create()
        self.assertIsInstance(project_entry_request, ProjectEntryRequest)
        self.assertEqual(project_entry_request.pk, 1)

        # test delete
        project_entry_request.delete()
        self.assertFalse(ProjectEntryRequest.objects.exists())

    def test_fields(self):
        project_entry_request = ProjectEntryRequest.objects.create()

        message = "I would love to contribute to this project as a software developer."
        project = Project.objects.create()
        profile = User.objects.create().profile

        project_entry_request.message = message
        project_entry_request.project = project
        project_entry_request.profile = profile

        project_entry_request.save()

        self.assertEqual(project_entry_request.message, message)
        self.assertEqual(project_entry_request.project, project)
        self.assertEqual(project_entry_request.profile, profile)

    def test_project_relation(self):
        project = Project.objects.create()
        project_entry_request = ProjectEntryRequest.objects.create(project=project)

        # testing related name
        self.assertIn(project_entry_request, project.entry_requests.all())

        # testing cascade
        project.delete()
        self.assertFalse(ProjectEntryRequest.objects.exists())

    def test_profile_relation(self):
        profile = User.objects.create().profile
        project_entry_request = ProjectEntryRequest.objects.create(profile=profile)

        # testing related name
        self.assertIn(project_entry_request, profile.projects_entry_requests.all())

        # testing cascade
        profile.delete()
        self.assertFalse(ProjectEntryRequest.objects.exists())

    def test_str(self):
        project = Project.objects.create(name="Simulatomic")
        profile = User.objects.create(username="john_p").profile
        project_entry_request = ProjectEntryRequest.objects.create(project=project, profile=profile)
        self.assertEqual(str(project_entry_request), f"{project.name} [entry request] {profile.user.username}")


class TestProjectInvitation(TestCase):
    def test_create_delete(self):
        # test create
        project_invitation = ProjectInvitation.objects.create()
        self.assertIsInstance(project_invitation, ProjectInvitation)
        self.assertEqual(project_invitation.pk, 1)

        # test delete
        project_invitation.delete()
        self.assertFalse(ProjectInvitation.objects.exists())

    def test_fields(self):
        project_invitation = ProjectInvitation.objects.create()

        message = "I would love to contribute to this project as a software developer."
        project = Project.objects.create()
        sender = User.objects.create(username="peter").profile
        receiver = User.objects.create(username="jake").profile

        project_invitation.message = message
        project_invitation.project = project
        project_invitation.sender = sender
        project_invitation.receiver = receiver

        project_invitation.save()

        self.assertEqual(project_invitation.message, message)
        self.assertEqual(project_invitation.project, project)
        self.assertEqual(project_invitation.sender, sender)
        self.assertEqual(project_invitation.receiver, receiver)

    def test_project_relation(self):
        project = Project.objects.create()
        project_invitation = ProjectInvitation.objects.create(project=project)

        # testing related name
        self.assertIn(project_invitation, project.invitations.all())

        # testing cascade
        project.delete()
        self.assertFalse(ProjectInvitation.objects.exists())

    def test_profile_relation(self):
        sender = User.objects.create(username="peter").profile
        receiver = User.objects.create(username="jake").profile
        project_invitation = ProjectInvitation.objects.create(sender=sender, receiver=receiver)

        # testing related name
        self.assertIn(project_invitation, sender.sent_projects_invitations.all())
        self.assertIn(project_invitation, receiver.received_projects_invitations.all())

        # testing cascade
        sender.delete()
        self.assertFalse(ProjectInvitation.objects.exists())
        ProjectInvitation.objects.create(receiver=receiver)
        receiver.delete()
        self.assertFalse(ProjectInvitation.objects.exists())

    def test_str(self):
        project = Project.objects.create(name="Simulatomic")
        receiver = User.objects.create(username="john_p").profile
        project_invitation = ProjectInvitation.objects.create(project=project, receiver=receiver)
        self.assertEqual(str(project_invitation), f"{project.name} [invitation] {receiver.user.username}")


class TestLink(TestCase):
    def test_create_delete(self):
        # test create
        link = Link.objects.create()
        self.assertIsInstance(link, Link)
        self.assertEqual(link.pk, 1)

        # test delete
        link.delete()
        self.assertFalse(Link.objects.exists())

    def test_fields(self):
        link = Link.objects.create()

        name = "Github"
        href = "https://github.com/projectx"
        project = Project.objects.create()

        link.name = name
        link.href = href
        link.project = project

        link.save()

        self.assertEqual(link.name, name)
        self.assertEqual(link.href, href)
        self.assertEqual(link.project, project)

    def test_str(self):
        project = Project.objects.create()
        link = Link.objects.create(name="Figma Mockup", project=project)
        self.assertEqual(str(link), f"{link.name} - {link.project}")

    def test_project_relation(self):
        project = Project.objects.create()
        link = Link.objects.create(project=project)

        # testing related name
        self.assertIn(link, project.links.all())

        # testing cascade
        project.delete()
        self.assertFalse(Link.objects.exists())


class TestToolCategory(TestCase):
    def test_create_delete(self):
        # test create
        tool_category = ToolCategory.objects.create()
        self.assertIsInstance(tool_category, ToolCategory)
        self.assertEqual(tool_category.pk, 1)

        # test delete
        tool_category.delete()
        self.assertFalse(ToolCategory.objects.exists())

    def test_fields(self):
        tool_category = ToolCategory.objects.create()

        name = "Ferramentas de desenvolvimento"
        project = Project.objects.create()

        tool_category.name = name
        tool_category.project = project
        tool_category.save()

        self.assertEqual(tool_category.name, name)
        self.assertEqual(tool_category.project, project)

    def test_str(self):
        project = Project.objects.create()
        tool_category = ToolCategory.objects.create(name="Documentos em Nuvem", project=project)
        self.assertEqual(str(tool_category), f"{tool_category.name} - {tool_category.project}")

    def test_project_relation(self):
        project = Project.objects.create()
        tool_category = ToolCategory.objects.create(project=project)

        # testing related name
        self.assertIn(tool_category, project.tools_categories.all())

        # testing cascade
        project.delete()
        self.assertFalse(ToolCategory.objects.exists())


class TestTool(TestCase):
    def test_create_delete(self):
        # test create
        tool = Tool.objects.create()
        self.assertIsInstance(tool, Tool)
        self.assertEqual(tool.pk, 1)

        # test delete
        tool.delete()
        self.assertFalse(Tool.objects.exists())

    def test_fields(self):
        tool = Tool.objects.create()

        name = "Github"
        href = "https://github.com/projectx"
        category = ToolCategory.objects.create()

        tool.category = category
        tool.name = name
        tool.href = href

        tool.save()

        self.assertEqual(tool.category, category)
        self.assertEqual(tool.name, name)
        self.assertEqual(tool.href, href)

    def test_str(self):
        tool = Tool.objects.create(name="Figma Mockup")
        self.assertEqual(str(tool), tool.name)


class TestProjectStar(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        project_star = ProjectStar.objects.create()
        self.assertIsInstance(project_star, ProjectStar)
        self.assertEqual(project_star.pk, 1)
        self.assertFalse(project_star.visualized)
        self.assertLessEqual(now_aware, project_star.created_at)
        self.assertLessEqual(now_aware, project_star.updated_at)

        # test delete
        project_star.delete()
        self.assertFalse(ProjectStar.objects.exists())

    def test_fields(self):
        project_star = ProjectStar.objects.create()

        profile = User.objects.create().profile
        project = Project.objects.create()
        visualized = True

        project_star.profile = profile
        project_star.project = project
        project_star.visualized = visualized

        project_star.save()

        self.assertEqual(project_star.profile, profile)
        self.assertEqual(project_star.project, project)
        self.assertTrue(project_star.visualized)

    def test_profile_relation(self):
        profile = User.objects.create().profile
        project_star = ProjectStar.objects.create(profile=profile)

        # testing related name
        self.assertIn(project_star, profile.projects_stars.all())

        # testing cascade
        profile.delete()
        self.assertFalse(ProjectStar.objects.exists())

    def test_project_relation(self):
        project = Project.objects.create()
        project_star = ProjectStar.objects.create(project=project)

        # testing related name
        self.assertIn(project_star, project.stars.all())

        # testing cascade
        project.delete()
        self.assertFalse(ProjectStar.objects.exists())

    def test_str(self):
        profile = User.objects.create(username="richard").profile

        project = Project.objects.create(name="Simulantum")

        project_star = ProjectStar.objects.create(profile=profile, project=project)
        self.assertEqual(str(project_star), f"{profile.user.username} starred {project}")


class TestDiscussion(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        discussion = Discussion.objects.create()
        self.assertIsInstance(discussion, Discussion)
        self.assertEqual(discussion.pk, 1)
        self.assertLessEqual(now_aware, discussion.created_at)
        self.assertLessEqual(now_aware, discussion.updated_at)

        # test delete
        discussion.delete()
        self.assertFalse(Discussion.objects.exists())

    def test_fields(self):
        discussion = Discussion.objects.create()

        title = "Projeto interessante, mas não entendi muito bem a parte da monetização."
        body = "Descrição detalhada..."
        category = "doubt"
        user = User.objects.create()
        project = Project.objects.create()

        discussion.title = title
        discussion.body = body
        discussion.category = category
        discussion.profile = user.profile
        discussion.project = project

        discussion.save()

        self.assertEqual(discussion.title, title)
        self.assertEqual(discussion.body, body)
        self.assertEqual(discussion.category, category)
        self.assertEqual(discussion.profile, user.profile)
        self.assertEqual(discussion.project, project)

    def test_profile_relation(self):
        profile = User.objects.create().profile
        discussion = Discussion.objects.create(profile=profile)

        # testing related name
        self.assertIn(discussion, profile.discussions.all())

        # testing cascade
        profile.delete()
        self.assertFalse(Discussion.objects.exists())

    def test_project_relation(self):
        project = Project.objects.create()
        discussion = Discussion.objects.create(project=project)

        # testing related name
        self.assertIn(discussion, project.discussions.all())

        # testing cascade
        project.delete()
        self.assertFalse(Discussion.objects.exists())

    def test_get_discussion_categories_choices_staticmethod(self):
        self.assertEqual(
            Discussion.get_discussion_categories_choices(),
            discussion_categories_choices,
        )

        self.assertEqual(
            Discussion.get_discussion_categories_choices(index=0),
            [discussion_category[0] for discussion_category in discussion_categories_choices],
        )

        self.assertEqual(
            Discussion.get_discussion_categories_choices(index=1),
            [discussion_category[1] for discussion_category in discussion_categories_choices],
        )

    def test_str(self):
        profile = User.objects.create(username="mark").profile
        discussion = Discussion.objects.create(
            title="I don't really understood why u guys r different...", profile=profile
        )
        self.assertEqual(str(discussion), f"{discussion.profile.user.username} - {discussion.title}")

    def test_category_value_and_readable_method(self):
        discussion = Discussion.objects.create(category=discussion_categories_choices[0][0])
        self.assertEqual(
            discussion.category_value_and_readable,
            {"value": discussion_categories_choices[0][0], "readable": discussion_categories_choices[0][1]},
        )


class TestDiscussionStar(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        discussion_star = DiscussionStar.objects.create()
        self.assertIsInstance(discussion_star, DiscussionStar)
        self.assertEqual(discussion_star.pk, 1)
        self.assertFalse(discussion_star.visualized)
        self.assertLessEqual(now_aware, discussion_star.created_at)
        self.assertLessEqual(now_aware, discussion_star.updated_at)

        # test delete
        discussion_star.delete()
        self.assertFalse(DiscussionStar.objects.exists())

    def test_fields(self):
        discussion_star = DiscussionStar.objects.create()

        profile = User.objects.create().profile
        discussion = Discussion.objects.create()
        visualized = True

        discussion_star.profile = profile
        discussion_star.discussion = discussion
        discussion_star.visualized = visualized

        discussion_star.save()

        self.assertEqual(discussion_star.profile, profile)
        self.assertEqual(discussion_star.discussion, discussion)
        self.assertTrue(discussion_star.visualized)

    def test_profile_relation(self):
        profile = User.objects.create().profile
        discussion_star = DiscussionStar.objects.create(profile=profile)

        # testing related name
        self.assertIn(discussion_star, profile.discussions_stars.all())

        # testing cascade
        profile.delete()
        self.assertFalse(DiscussionStar.objects.exists())

    def test_discussion_relation(self):
        discussion = Discussion.objects.create()
        discussion_star = DiscussionStar.objects.create(discussion=discussion)

        # testing related name
        self.assertIn(discussion_star, discussion.stars.all())

        # testing cascade
        discussion.delete()
        self.assertFalse(DiscussionStar.objects.exists())

    def test_str(self):
        profile01 = User.objects.create(username="richard").profile

        profile02 = User.objects.create(username="mark").profile
        discussion = Discussion.objects.create(title="Lorem ipsum dolor sit amet", profile=profile02)

        discussion_star = DiscussionStar.objects.create(profile=profile01, discussion=discussion)
        self.assertEqual(str(discussion_star), f"{profile01.user.username} starred {discussion}")


class TestDiscussionReply(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        discussion_reply = DiscussionReply.objects.create()
        self.assertIsInstance(discussion_reply, DiscussionReply)
        self.assertEqual(discussion_reply.pk, 1)
        self.assertFalse(discussion_reply.visualized)
        self.assertLessEqual(now_aware, discussion_reply.created_at)
        self.assertLessEqual(now_aware, discussion_reply.updated_at)

        # test delete
        discussion_reply.delete()
        self.assertFalse(DiscussionReply.objects.exists())

    def test_fields(self):
        discussion_reply = DiscussionReply.objects.create()

        content = "Lorem ipsum dolor sit amet"
        profile = User.objects.create().profile
        discussion = Discussion.objects.create()
        visualized = True

        discussion_reply.content = content
        discussion_reply.profile = profile
        discussion_reply.discussion = discussion
        discussion_reply.visualized = visualized

        discussion_reply.save()

        self.assertEqual(discussion_reply.content, content)
        self.assertEqual(discussion_reply.profile, profile)
        self.assertEqual(discussion_reply.discussion, discussion)
        self.assertTrue(discussion_reply.visualized)

    def test_profile_relation(self):
        profile = User.objects.create().profile
        discussion_reply = DiscussionReply.objects.create(profile=profile)

        # testing related name
        self.assertIn(discussion_reply, profile.discussions_replies.all())

        # testing cascade
        profile.delete()
        self.assertFalse(DiscussionReply.objects.exists())

    def test_discussion_relation(self):
        discussion = Discussion.objects.create()
        discussion_reply = DiscussionReply.objects.create(discussion=discussion)

        # testing related name
        self.assertIn(discussion_reply, discussion.replies.all())

        # testing cascade
        discussion.delete()
        self.assertFalse(DiscussionReply.objects.exists())

    def test_str(self):
        profile01 = User.objects.create(username="richard").profile

        profile02 = User.objects.create(username="mark").profile
        discussion = Discussion.objects.create(title="Lorem ipsum dolor sit amet" * 10, profile=profile02)

        discussion_reply = DiscussionReply.objects.create(
            content="Foo bar" * 10, profile=profile01, discussion=discussion
        )
        self.assertEqual(
            str(discussion_reply),
            f"{profile01.user.username} replied {discussion_reply.content[:50]} to {discussion.title[:50]}",
        )
