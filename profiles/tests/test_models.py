import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from profiles.models import Mentor, Profile, Student
from universities.models import MajorField, University


class TestModels(TestCase):
    def setUp(self):
        self.User = get_user_model()

    # User model
    def test_create_user(self):
        username = "joao"
        user = self.User.objects.create(username=username, password="secret")
        self.assertIsInstance(user, self.User)
        self.assertEqual(user.username, username)
        self.assertTrue(user.is_active)

        # testing username unique constrain
        self.assertRaises(IntegrityError, self.User.objects.create, username=username)

    def test_create_profile_signal(self):
        user = self.User.objects.create()

        self.assertEqual(Profile.objects.get(user=user), user.profile)

    def test_delete_user(self):
        user01 = self.User.objects.create(username="a")
        user02 = self.User.objects.create(username="b")
        user03 = self.User.objects.create(username="c")

        self.assertEqual(list(self.User.objects.all()), [user01, user02, user03])

        user02.delete()

        self.assertEqual(list(self.User.objects.all()), [user01, user03])

    # Profile model
    def test_create_profile(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        user = self.User.objects.create()
        profile = user.profile

        first_name = "Elon"
        last_name = "Musk"
        birth_date = "1950-01-01"
        email = "elon@tesla.com"

        profile.first_name = first_name
        profile.last_name = last_name
        profile.birth_date = birth_date
        profile.email = email

        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.first_name, first_name)
        self.assertEqual(profile.last_name, last_name)
        self.assertEqual(profile.birth_date, birth_date)
        self.assertEqual(profile.email, email)
        self.assertLessEqual(now_aware, profile.created_at)
        self.assertLessEqual(now_aware, profile.updated_at)

        # testing email unique constrain
        self.assertRaises(IntegrityError, Profile.objects.create, email=email)

    def test_delete_profile(self):
        user01 = self.User.objects.create(username="a")
        user02 = self.User.objects.create(username="b")
        user03 = self.User.objects.create(username="c")

        self.assertEqual(list(Profile.objects.all()), [user01.profile, user02.profile, user03.profile])

        user02.profile.delete()

        self.assertEqual(list(Profile.objects.all()), [user01.profile, user03.profile])

        user03.delete()  # testing models.CASCADE

        self.assertEqual(list(Profile.objects.all()), [user01.profile])

    # Student model
    def test_create_student(self):
        user = self.User.objects.create()
        university = University.objects.create()

        student = Student.objects.create(profile=user.profile, university=university)

        self.assertIsInstance(student, Student)
        self.assertEqual(student.profile, user.profile)
        self.assertEqual(student.university, university)

        # testing related name
        self.assertEqual(user.profile.student, student)

    def test_delete_student(self):
        user01 = self.User.objects.create(username="a")
        user02 = self.User.objects.create(username="b")
        user03 = self.User.objects.create(username="c")

        student01 = Student.objects.create(profile=user01.profile)
        student02 = Student.objects.create(profile=user02.profile)
        student03 = Student.objects.create(profile=user03.profile)

        self.assertEqual(list(Student.objects.all()), [student01, student02, student03])

        student02.delete()

        self.assertEqual(list(Student.objects.all()), [student01, student03])

        user03.profile.delete()  # testing models.CASCADE

        self.assertEqual(list(Student.objects.all()), [student01])

        user01.delete()

        self.assertEqual(list(Student.objects.all()), [])

    # Mentor model
    def test_create_mentor(self):
        user = self.User.objects.create()
        expertise = MajorField.objects.create()

        mentor = Mentor.objects.create(profile=user.profile, expertise=expertise)

        self.assertIsInstance(mentor, Mentor)
        self.assertEqual(mentor.profile, user.profile)
        self.assertEqual(mentor.expertise, expertise)

        # testing related name
        self.assertEqual(user.profile.mentor, mentor)

    def test_delete_mentor(self):
        user01 = self.User.objects.create(username="a")
        user02 = self.User.objects.create(username="b")
        user03 = self.User.objects.create(username="c")

        mentor01 = Mentor.objects.create(profile=user01.profile)
        mentor02 = Mentor.objects.create(profile=user02.profile)
        mentor03 = Mentor.objects.create(profile=user03.profile)

        self.assertEqual(list(Mentor.objects.all()), [mentor01, mentor02, mentor03])

        mentor02.delete()

        self.assertEqual(list(Mentor.objects.all()), [mentor01, mentor03])

        mentor03.profile.delete()  # testing models.CASCADE

        self.assertEqual(list(Mentor.objects.all()), [mentor01])

        user01.delete()

        self.assertEqual(list(Mentor.objects.all()), [])
