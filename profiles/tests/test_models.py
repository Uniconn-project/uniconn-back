import datetime
from time import sleep

import pytz
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from universities.models import Major, University

from ..models import Mentor, Profile, Student

User = get_user_model()


class TestUser(TestCase):
    def test_create_delete(self):
        # test create
        user = User.objects.create()
        self.assertIsInstance(user, User)
        self.assertEqual(user.pk, 1)
        self.assertTrue(user.is_active)

        # test delete
        user.delete()
        self.assertFalse(User.objects.filter().exists())

    def test_fields(self):
        user = User.objects.create()

        username = "john"
        email = "john@test.com"
        user.username = username
        user.email = email
        user.is_active = False
        user.set_password("secret")
        user.save()

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertFalse(user.is_active)

        # testing username unique constrain
        with transaction.atomic():
            self.assertRaises(IntegrityError, User.objects.create, username=username)


class TestProfile(TestCase):
    def test_create_delete(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        user = User.objects.create()
        profile = user.profile
        self.assertIsInstance(profile, Profile)
        self.assertEqual(profile.pk, 1)
        self.assertEqual(profile.photo, "profile_avatar.jpeg")
        self.assertEqual(profile.bio, "Sem bio...")
        self.assertLessEqual(now_aware, profile.created_at)
        self.assertLessEqual(now_aware, profile.updated_at)

        # test delete
        profile.delete()
        self.assertFalse(Profile.objects.filter().exists())

    def test_fields(self):
        user = User.objects.create()
        profile = user.profile

        photo = "elon_musk.jpg"
        first_name = "Elon"
        last_name = "Musk"
        bio = "Space-X, Tesla and Neuralink"
        linkedIn = "elon-musk28061971"
        birth_date = "1971-06-28"

        profile.photo = photo
        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        profile.linkedIn = linkedIn
        profile.birth_date = birth_date
        profile.save()

        self.assertEqual(profile.photo, photo)
        self.assertEqual(profile.first_name, first_name)
        self.assertEqual(profile.last_name, last_name)
        self.assertEqual(profile.bio, bio)
        self.assertEqual(profile.linkedIn, linkedIn)
        self.assertEqual(profile.birth_date, birth_date)

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

    def test_type_method(self):
        user01 = User.objects.create()
        Student.objects.create(profile=user01.profile)
        self.assertEqual(user01.profile.type, "student")

        user02 = User.objects.create(username="jack")
        Mentor.objects.create(profile=user02.profile)
        self.assertEqual(user02.profile.type, "mentor")


class TestStudent(TestCase):
    def test_create_delete(self):
        # test create
        user = User.objects.create()
        student = Student.objects.create(profile=user.profile)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.pk, 1)
        self.assertEqual(student.profile, user.profile)

        # test delete
        student.delete()
        self.assertFalse(Student.objects.filter().exists())

    def test_fields(self):
        user = User.objects.create()
        student = Student.objects.create(profile=user.profile)

        university = University.objects.create()
        major = Major.objects.create()

        student.university = university
        student.major = major
        student.save()

        self.assertEqual(student.university, university)
        self.assertEqual(student.major, major)

    def test_student_profile_relationship(self):
        # Asserting the student-profile relationship is one to one
        user = User.objects.create()
        profile = user.profile
        Student.objects.create(profile=profile)
        with transaction.atomic():
            self.assertRaises(IntegrityError, Student.objects.create, profile=profile)

        self.assertEqual(profile.student.profile, profile, "Asserting the student-profile related name is 'student'")

        profile.delete()
        self.assertFalse(
            Student.objects.filter().exists(), "Asserting the student-profile relationship cascades on delete"
        )

    def test_str(self):
        user = User.objects.create(username="caroline")
        student = Student.objects.create(profile=user.profile)
        self.assertEqual(str(student), f"{user.username} [STUDENT]")

    def test_ordering(self):
        user01 = User.objects.create(username="lincoln")
        student01 = Student.objects.create(profile=user01.profile)

        sleep(0.001)

        user02 = User.objects.create(username="alex")
        student02 = Student.objects.create(profile=user02.profile)

        self.assertEqual(list(Student.objects.all()), [student02, student01])


class TestMentor(TestCase):
    def test_create_delete(self):
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
        Mentor.objects.create(profile=profile)
        with transaction.atomic():
            self.assertRaises(IntegrityError, Mentor.objects.create, profile=profile)

        self.assertEqual(profile.mentor.profile, profile, "Asserting the mentor-profile related name is 'mentor'")

        profile.delete()
        self.assertFalse(
            Mentor.objects.filter().exists(), "Asserting the mentor-profile relationship cascades on delete"
        )

    def test_str(self):
        user = User.objects.create(username="michael")
        mentor = Mentor.objects.create(profile=user.profile)
        self.assertEqual(str(mentor), f"{user.username} [MENTOR]")

    def test_ordering(self):
        user01 = User.objects.create(username="dianne")
        mentor01 = Mentor.objects.create(profile=user01.profile)

        sleep(0.001)

        user02 = User.objects.create(username="kevin")
        mentor02 = Mentor.objects.create(profile=user02.profile)

        self.assertEqual(list(Mentor.objects.all()), [mentor02, mentor01])
