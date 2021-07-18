import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from profiles.models import Mentor, Student
from projects.models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Link,
    Market,
    Project,
    ProjectEnteringRequest,
    ProjectStar,
    Tool,
    discussion_categories_choices,
    project_categories_choices,
    tool_categories_choices,
)

User = get_user_model()


class TestMarket(TestCase):
    def test_create_delete(self):
        # test create
        market = Market.objects.create()
        self.assertIsInstance(market, Market)
        self.assertEqual(market.pk, 1)

        # test delete
        market.delete()
        self.assertFalse(Market.objects.exists())

    def test_fields(self):
        market = Market.objects.create()

        user01 = User.objects.create()
        mentor01 = Mentor.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="john")
        mentor02 = Mentor.objects.create(profile=user02.profile)

        market.mentors.add(mentor01, mentor02)

        name = "Education"
        market.name = name

        market.save()

        self.assertEqual(market.name, name.lower())
        self.assertEqual(len(market.mentors.all()), 2)
        self.assertIn(mentor01, market.mentors.all())
        self.assertIn(mentor02, market.mentors.all())

        # testing name unique constrain
        with transaction.atomic():
            self.assertRaises(IntegrityError, Market.objects.create, name=name)

    def test_related_name(self):
        user = User.objects.create()
        mentor = Mentor.objects.create(profile=user.profile)
        market = Market.objects.create()
        market.mentors.add(mentor)

        self.assertIn(market, mentor.markets.all())

    def test_str(self):
        market = Market.objects.create(name="Innovation")
        self.assertEqual(str(market), market.name)


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

        link.name = name
        link.href = href

        link.save()

        self.assertEqual(link.name, name)
        self.assertEqual(link.href, href)

    def test_str(self):
        link = Link.objects.create(name="Figma Mockup")
        self.assertEqual(str(link), link.name)


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
        category = "development_tools"

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

    def test_category_value_and_readable_method(self):
        tool = Tool.objects.create(category=tool_categories_choices[0][0])
        self.assertEqual(
            tool.category_value_and_readable,
            {"value": tool_categories_choices[0][0], "readable": tool_categories_choices[0][1]},
        )


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

        user01 = User.objects.create()
        user02 = User.objects.create(username="mark")

        student01 = Student.objects.create(profile=user01.profile)
        student02 = Student.objects.create(profile=user02.profile)
        project.students.add(student01)
        project.pending_invited_students.add(student02)

        user03 = User.objects.create(username="jessica")
        user04 = User.objects.create(username="simon")

        mentor01 = Mentor.objects.create(profile=user03.profile)
        mentor02 = Mentor.objects.create(profile=user04.profile)
        project.mentors.add(mentor01)
        project.pending_invited_mentors.add(mentor02)

        market01 = Market.objects.create(name="agriculture")
        market02 = Market.objects.create(name="computer-brain interface")
        project.markets.add(market01, market02)

        link01 = Link.objects.create()
        link02 = Link.objects.create()
        project.links.add(link01, link02)

        tool01 = Tool.objects.create()
        tool02 = Tool.objects.create()
        project.tools.add(tool01, tool02)

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

        self.assertEqual(list(project.students.all()), [student01])
        self.assertEqual(list(project.pending_invited_students.all()), [student02])
        self.assertEqual(list(project.mentors.all()), [mentor01])
        self.assertEqual(list(project.pending_invited_mentors.all()), [mentor02])
        self.assertEqual(list(project.markets.all()), [market01, market02])
        self.assertEqual(list(project.links.all()), [link01, link02])
        self.assertEqual(list(project.tools.all()), [tool01, tool02])

    def test_related_name(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="nelson")
        user02 = User.objects.create(username="john")
        user03 = User.objects.create(username="marie")
        user04 = User.objects.create(username="peter")

        # students
        student01 = Student.objects.create(profile=user01.profile)
        project.students.add(student01)
        self.assertIn(project, student01.projects.all())

        # pending_invited_students
        student02 = Student.objects.create(profile=user02.profile)
        project.pending_invited_students.add(student02)
        self.assertIn(project, student02.pending_projects_invitations.all())

        # mentors
        mentor01 = Mentor.objects.create(profile=user03.profile)
        project.mentors.add(mentor01)
        self.assertIn(project, mentor01.projects.all())

        # pending_invited_mentors
        mentor02 = Mentor.objects.create(profile=user04.profile)
        project.pending_invited_mentors.add(mentor02)
        self.assertIn(project, mentor02.pending_projects_invitations.all())

        # markets
        market = Market.objects.create()
        project.markets.add(market)
        self.assertIn(project, market.projects.all())

        # links
        link = Link.objects.create()
        project.links.add(link)
        self.assertIn(project, link.projects.all())

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

    def test_category_value_and_readable_method(self):
        project = Project.objects.create(category=project_categories_choices[0][0])
        self.assertEqual(
            project.category_value_and_readable,
            {"value": project_categories_choices[0][0], "readable": project_categories_choices[0][1]},
        )

    def test_students_profiles_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="taylor")
        student01 = Student.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="peter")
        student02 = Student.objects.create(profile=user02.profile)

        project.students.add(student01, student02)
        project.save()

        students_profiles = project.students_profiles

        self.assertEqual(len(students_profiles), 2)
        self.assertIn(user01.profile, students_profiles)
        self.assertIn(user02.profile, students_profiles)

    def test_mentors_profiles_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="maicon")
        mentor01 = Mentor.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="joanne")
        mentor02 = Mentor.objects.create(profile=user02.profile)

        project.mentors.add(mentor01, mentor02)
        project.save()

        mentors_profiles = project.mentors_profiles

        self.assertEqual(len(mentors_profiles), 2)
        self.assertIn(user01.profile, mentors_profiles)
        self.assertIn(user02.profile, mentors_profiles)

    def test_pending_invited_students_profiles_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="taylor")
        student01 = Student.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="peter")
        student02 = Student.objects.create(profile=user02.profile)

        project.pending_invited_students.add(student01, student02)
        project.save()

        pending_invited_students_profiles = project.pending_invited_students_profiles

        self.assertEqual(len(pending_invited_students_profiles), 2)
        self.assertIn(user01.profile, pending_invited_students_profiles)
        self.assertIn(user02.profile, pending_invited_students_profiles)

    def test_pending_invited_mentors_profiles_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="maicon")
        mentor01 = Mentor.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="joanne")
        mentor02 = Mentor.objects.create(profile=user02.profile)

        project.pending_invited_mentors.add(mentor01, mentor02)
        project.save()

        pending_invited_mentors_profiles = project.pending_invited_mentors_profiles

        self.assertEqual(len(pending_invited_mentors_profiles), 2)
        self.assertIn(user01.profile, pending_invited_mentors_profiles)
        self.assertIn(user02.profile, pending_invited_mentors_profiles)

    def test_discussions_length_method(self):
        project = Project.objects.create()

        Discussion.objects.create(project=project)
        Discussion.objects.create(project=project)
        Discussion.objects.create(project=project)

        self.assertEqual(project.discussions_length, 3)


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


class TestProjectEnteringRequest(TestCase):
    def test_create_delete(self):
        # test create
        project_entering_request = ProjectEnteringRequest.objects.create()
        self.assertIsInstance(project_entering_request, ProjectEnteringRequest)
        self.assertEqual(project_entering_request.pk, 1)

        # test delete
        project_entering_request.delete()
        self.assertFalse(ProjectEnteringRequest.objects.exists())

    def test_fields(self):
        project_entering_request = ProjectEnteringRequest.objects.create()

        message = "I would love to contribute to this project as a software developer."
        project = Project.objects.create()
        user = User.objects.create()

        project_entering_request.message = message
        project_entering_request.project = project
        project_entering_request.profile = user.profile

        project_entering_request.save()

        self.assertEqual(project_entering_request.message, message)
        self.assertEqual(project_entering_request.project, project)
        self.assertEqual(project_entering_request.profile, user.profile)

    def test_project_relation(self):
        project = Project.objects.create()
        project_entering_request = ProjectEnteringRequest.objects.create(project=project)

        # testing related name
        self.assertIn(project_entering_request, project.entering_requests.all())

        # testing cascade
        project.delete()
        self.assertFalse(ProjectEnteringRequest.objects.exists())

    def test_profile_relation(self):
        profile = User.objects.create().profile
        project_entering_request = ProjectEnteringRequest.objects.create(profile=profile)

        # testing related name
        self.assertIn(project_entering_request, profile.projects_entering_requests.all())

        # testing cascade
        profile.delete()
        self.assertFalse(ProjectEnteringRequest.objects.exists())

    def test_str(self):
        project = Project.objects.create(name="Simutomic")
        user = User.objects.create(username="john_p")
        project_entering_request = ProjectEnteringRequest.objects.create(project=project, profile=user.profile)
        self.assertEqual(str(project_entering_request), f"{user.username} to {project.name}")


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
