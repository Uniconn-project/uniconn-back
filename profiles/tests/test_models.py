import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from profiles.models import Mentor, Profile, Student
from universities.models import Major, University

User = get_user_model()


class TestUser(TestCase):
    def setUp(self):
        pass

    def test_model(self):
        # test create
        user = User.objects.create()
        self.assertIsInstance(user, User)
        self.assertEqual(user.pk, 1)
        self.assertTrue(user.is_active)

        # test edit
        username = "joão"
        user.username = username
        user.is_active = False
        user.set_password("secret")
        user.save()

        self.assertEqual(user.username, username)
        self.assertFalse(user.is_active)

        # testing username unique constrain
        with transaction.atomic():
            self.assertRaises(IntegrityError, User.objects.create, username=username)

        # test delete
        user.delete()
        self.assertFalse(User.objects.filter().exists())


class TestProfile(TestCase):
    def setUp(self):
        pass

    def test_model(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        user = User.objects.create()
        profile = user.profile
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.pk, 1)
        self.assertEqual(profile.photo, "profile_avatar.jpg")
        self.assertLessEqual(now_aware, profile.created_at)
        self.assertLessEqual(now_aware, profile.updated_at)

        # test edit
        first_name = "Elon"
        last_name = "Musk"
        birth_date = "1971-06-28"
        email = "elon@tesla.com"
        photo = "data:image/png;base64,iVBORw0KGg===="

        profile.first_name = first_name
        profile.last_name = last_name
        profile.photo = photo
        profile.birth_date = birth_date
        profile.email = email

        self.assertEqual(profile.first_name, first_name)
        self.assertEqual(profile.last_name, last_name)
        self.assertEqual(profile.photo, photo)
        self.assertEqual(profile.birth_date, birth_date)
        self.assertEqual(profile.email, email)

        # testing email unique constrain
        with transaction.atomic():
            self.assertRaises(IntegrityError, Profile.objects.create, email=email)

        # test delete
        profile.delete()
        self.assertFalse(Profile.objects.filter().exists())

    def test_profile_user_relationship(self):
        # Asserting the profile-user relationship is one to one
        user = User.objects.create()
        with transaction.atomic():
            self.assertRaises(IntegrityError, Profile.objects.create, user=user)

        self.assertEqual(user.profile.user, user, "Asserting the profile-user related name is 'profile'")

        user.delete()
        self.assertFalse(
            Profile.objects.filter().exists(), "Asserting the profile-user relationship cascades on delete"
        )

    def test_str(self):
        user = User.objects.create()
        profile = user.profile
        self.assertEqual(str(profile), profile.user.username)


class TestStudent(TestCase):
    def setUp(self):
        pass

    def test_model(self):
        # test create
        user = User.objects.create()
        profile = user.profile
        student = Student.objects.create(profile=profile)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.pk, 1)
        self.assertEqual(student.profile, profile)

        # test edit
        university = University.objects.create()
        major = Major.objects.create()

        student.university = university
        student.major = major
        student.save()

        self.assertEqual(student.university, university)
        self.assertEqual(student.major, major)

        # test delete
        student.delete()
        self.assertFalse(Student.objects.filter().exists())

    def test_student_profile_relationship(self):
        # Asserting the student-profile relationship is one to one
        user = User.objects.create()
        profile = user.profile
        student = Student.objects.create(profile=profile)
        with transaction.atomic():
            self.assertRaises(IntegrityError, Student.objects.create, profile=profile)

        self.assertEqual(profile.student.profile, profile, "Asserting the student-profile related name is 'student'")

        profile.delete()
        self.assertFalse(
            Student.objects.filter().exists(), "Asserting the student-profile relationship cascades on delete"
        )


class TestMentor(TestCase):
    def setUp(self):
        pass

    def test_model(self):
        # test create
        user = User.objects.create()
        profile = user.profile
        mentor = Mentor.objects.create(profile=profile)
        self.assertIsInstance(mentor, Mentor)
        self.assertEqual(mentor.pk, 1)
        self.assertEqual(mentor.profile, profile)

        # test delete
        mentor.delete()
        self.assertFalse(Mentor.objects.filter().exists())

    def test_mentor_profile_relationship(self):
        # Asserting the mentor-profile relationship is one to one
        user = User.objects.create()
        profile = user.profile
        mentor = Mentor.objects.create(profile=profile)
        with transaction.atomic():
            self.assertRaises(IntegrityError, Mentor.objects.create, profile=profile)

        self.assertEqual(profile.mentor.profile, profile, "Asserting the mentor-profile related name is 'mentor'")

        profile.delete()
        self.assertFalse(
            Mentor.objects.filter().exists(), "Asserting the mentor-profile relationship cascades on delete"
        )
