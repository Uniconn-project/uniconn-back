import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from projects.models import Project, ProjectMember
from universities.models import Major, University

from ..models import Profile, Skill

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
        self.assertFalse(User.objects.exists())

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


class TestSkill(TestCase):
    def test_create_delete(self):
        # test create
        skill = Skill.objects.create()
        self.assertIsInstance(skill, Skill)
        self.assertEqual(skill.pk, 1)

        # test delete
        skill.delete()
        self.assertFalse(Skill.objects.exists())

    def test_fields(self):
        skill = Skill.objects.create()

        name = "Programming"
        skill.name = name
        skill.save()

        self.assertEqual(skill.name, name.lower())

        # testing name unique constrain
        with transaction.atomic():
            self.assertRaises(IntegrityError, Skill.objects.create, name=name)

    def test_str(self):
        skill = Skill.objects.create()
        self.assertEqual(str(skill), skill.name)

    def test_ordering(self):
        skill01 = Skill.objects.create(name="design")
        skill02 = Skill.objects.create(name="coding")

        self.assertEqual(list(Skill.objects.all()), [skill02, skill01])


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
        self.assertFalse(Profile.objects.exists())

    def test_fields(self):
        user = User.objects.create()
        profile = user.profile

        photo = "elon_musk.jpg"
        first_name = "Elon"
        last_name = "Musk"
        bio = "Space-X, Tesla and Neuralink"
        birth_date = "1971-06-28"
        linkedIn = "elon-musk28061971"
        skills = [Skill.objects.create(name="business"), Skill.objects.create(name="design")]
        is_attending_university = True
        university = University.objects.create()
        major = Major.objects.create()

        profile.photo = photo
        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        profile.birth_date = birth_date
        profile.linkedIn = linkedIn
        profile.skills.set(skills)
        profile.is_attending_university = is_attending_university
        profile.university = university
        profile.major = major
        profile.save()

        self.assertEqual(profile.photo, photo)
        self.assertEqual(profile.first_name, first_name)
        self.assertEqual(profile.last_name, last_name)
        self.assertEqual(profile.bio, bio)
        self.assertEqual(profile.birth_date, birth_date)
        self.assertEqual(profile.linkedIn, linkedIn)
        self.assertEqual(list(profile.skills.all()), skills)
        self.assertEqual(profile.is_attending_university, is_attending_university)
        self.assertEqual(profile.university, university)
        self.assertEqual(profile.major, major)

    def test_profile_user_relationship(self):
        # Asserting the profile-user relationship is one to one
        user = User.objects.create()
        with transaction.atomic():
            self.assertRaises(IntegrityError, Profile.objects.create, user=user)

        self.assertEqual(user.profile.user, user, "Asserting the profile-user related name is 'profile'")

        user.delete()
        self.assertFalse(Profile.objects.exists(), "Asserting the profile-user relationship cascades on delete")

    def test_str(self):
        user = User.objects.create()
        profile = user.profile
        self.assertEqual(str(profile), profile.user.username)

    def test_projects_method(self):
        profile = User.objects.create().profile
        project01 = Project.objects.create()
        project02 = Project.objects.create()

        ProjectMember.objects.create(profile=profile, project=project01)
        ProjectMember.objects.create(profile=profile, project=project02)

        self.assertEqual(profile.projects, [project01, project02])
