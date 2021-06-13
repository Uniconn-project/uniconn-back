import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from profiles.models import Mentor, Student
from projects.models import Link, Market, Project, project_categories_choices

User = get_user_model()


class TestMarket(TestCase):
    def test_create_delete(self):
        # test create
        market = Market.objects.create()
        self.assertIsInstance(market, Market)
        self.assertEqual(market.pk, 1)

        # test delete
        market.delete()
        self.assertFalse(Market.objects.filter().exists())

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
        self.assertFalse(Link.objects.filter().exists())

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


class TestProject(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        project = Project.objects.create()
        self.assertIsInstance(project, Project)
        self.assertEqual(project.pk, 1)
        self.assertEqual(project.image, "default_project.jpg")
        self.assertLessEqual(now_aware, project.created_at)
        self.assertLessEqual(now_aware, project.updated_at)

        # test delete
        project.delete()
        self.assertFalse(Project.objects.filter().exists())

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

        market01 = Market.objects.create()
        market02 = Market.objects.create()
        project.markets.add(market01, market02)

        link01 = Link.objects.create()
        link02 = Link.objects.create()
        project.links.add(link01, link02)

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

    def test_related_name(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="nelson")
        user02 = User.objects.create(username="john")
        user03 = User.objects.create(username="marie")
        user04 = User.objects.create(username="peter")

        student01 = Student.objects.create(profile=user01.profile)
        project.students.add(student01)
        self.assertIn(project, student01.projects.all())

        student02 = Student.objects.create(profile=user02.profile)
        project.pending_invited_students.add(student02)
        self.assertIn(project, student02.pending_projects_invitations.all())

        mentor01 = Mentor.objects.create(profile=user03.profile)
        project.mentors.add(mentor01)
        self.assertIn(project, mentor01.projects.all())

        mentor02 = Mentor.objects.create(profile=user04.profile)
        project.pending_invited_mentors.add(mentor02)
        self.assertIn(project, mentor02.pending_projects_invitations.all())

        market = Market.objects.create()
        project.markets.add(market)
        self.assertIn(project, market.projects.all())

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

    def test_students_profile_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="taylor")
        student01 = Student.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="peter")
        student02 = Student.objects.create(profile=user02.profile)

        project.students.add(student01, student02)
        project.save()

        students_profile = project.students_profile

        self.assertEqual(len(students_profile), 2)
        self.assertIn(user01.profile, students_profile)
        self.assertIn(user02.profile, students_profile)

    def test_mentors_profile_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="maicon")
        mentor01 = Mentor.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="joanne")
        mentor02 = Mentor.objects.create(profile=user02.profile)

        project.mentors.add(mentor01, mentor02)
        project.save()

        mentors_profile = project.mentors_profile

        self.assertEqual(len(mentors_profile), 2)
        self.assertIn(user01.profile, mentors_profile)
        self.assertIn(user02.profile, mentors_profile)

    def test_pending_invited_students_profile_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="taylor")
        student01 = Student.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="peter")
        student02 = Student.objects.create(profile=user02.profile)

        project.pending_invited_students.add(student01, student02)
        project.save()

        pending_invited_students_profile = project.pending_invited_students_profile

        self.assertEqual(len(pending_invited_students_profile), 2)
        self.assertIn(user01.profile, pending_invited_students_profile)
        self.assertIn(user02.profile, pending_invited_students_profile)

    def test_pending_invited_mentors_profile_method(self):
        project = Project.objects.create()

        user01 = User.objects.create(username="maicon")
        mentor01 = Mentor.objects.create(profile=user01.profile)

        user02 = User.objects.create(username="joanne")
        mentor02 = Mentor.objects.create(profile=user02.profile)

        project.pending_invited_mentors.add(mentor01, mentor02)
        project.save()

        pending_invited_mentors_profile = project.pending_invited_mentors_profile

        self.assertEqual(len(pending_invited_mentors_profile), 2)
        self.assertIn(user01.profile, pending_invited_mentors_profile)
        self.assertIn(user02.profile, pending_invited_mentors_profile)
