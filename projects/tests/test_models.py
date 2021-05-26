import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from profiles.models import Mentor, Student
from projects.models import Market, Project, project_categories_choices

User = get_user_model()


class TestMarket(TestCase):
    def test_model(self):
        # test create
        market = Market.objects.create()
        self.assertIsInstance(market, Market)
        self.assertEqual(market.pk, 1)

        # test edit
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

        # test delete
        market.delete()
        self.assertFalse(Market.objects.filter().exists())

    def test_related_name(self):
        user = User.objects.create()
        mentor = Mentor.objects.create(profile=user.profile)
        market = Market.objects.create()
        market.mentors.add(mentor)

        self.assertIn(market, mentor.markets.all())

    def test_str(self):
        market = Market.objects.create(name="Innovation")
        self.assertEqual(str(market), market.name)


class TestProject(TestCase):
    def test_model(self):
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

        # test edit
        category = "startup"
        name = "4Share"
        slogan = "Awesome technologies 4 share"
        description = "Detailed description..."
        image = "4share_logo.jpeg"

        user01 = User.objects.create()
        user02 = User.objects.create(username="mark")

        student01 = Student.objects.create(profile=user01.profile)
        student02 = Student.objects.create(profile=user02.profile)
        project.students.add(student01, student02)

        user03 = User.objects.create(username="jessica")
        user04 = User.objects.create(username="simon")

        mentor01 = Mentor.objects.create(profile=user03.profile)
        mentor02 = Mentor.objects.create(profile=user04.profile)
        project.mentors.add(mentor01, mentor02)

        market01 = Market.objects.create()
        market02 = Market.objects.create()
        project.markets.add(market01, market02)

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

        students = project.students.all()
        self.assertEqual(len(students), 2)
        self.assertIn(student01, students)
        self.assertIn(student02, students)

        mentors = project.mentors.all()
        self.assertEqual(len(mentors), 2)
        self.assertIn(mentor01, mentors)
        self.assertIn(mentor02, mentors)

        markets = project.markets.all()
        self.assertEqual(len(markets), 2)
        self.assertIn(market01, markets)
        self.assertIn(market02, markets)

        # test delete
        project.delete()
        self.assertFalse(Project.objects.filter().exists())

    def test_related_name(self):
        project = Project.objects.create()
        user01 = User.objects.create(username="nelson")
        student = Student.objects.create(profile=user01.profile)
        project.students.add(student)
        self.assertIn(project, student.projects.all())

        user02 = User.objects.create(username="marie")
        mentor = Mentor.objects.create(profile=user02.profile)
        project.mentors.add(mentor)
        self.assertIn(project, mentor.projects.all())

        market = Market.objects.create()
        project.markets.add(market)
        self.assertIn(project, market.projects.all())

    def test_str(self):
        project = Project.objects.create(name="Uniconn")
        self.assertEqual(str(project), project.name)

    def test_get_project_categories_choices_staticmethod(self):
        self.assertEqual(
            Project.get_project_categories_choices(),
            [project_category for project_category in project_categories_choices],
        )

        self.assertEqual(
            Project.get_project_categories_choices(index=0),
            [project_category[0] for project_category in project_categories_choices],
        )

        self.assertEqual(
            Project.get_project_categories_choices(index=1),
            [project_category[1] for project_category in project_categories_choices],
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
