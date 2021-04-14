import datetime

import pytz
from django.db.utils import IntegrityError
from django.test import TestCase
from universities.models import Major, MajorField, University


class TestModels(TestCase):
    def setUp(self):
        pass

    # MajorField model
    def test_create_major(self):
        major = Major.objects.create()
        self.assertIsInstance(major, Major)
        self.assertIsNone(major.name)
        self.assertEqual(len(major.fields.all()), 0)

        name = "Computer Engeneering"
        major.name = name
        major_field01 = MajorField.objects.create(name="Coding")
        major_field02 = MajorField.objects.create(name="Engeneering")
        major.fields.add(major_field01, major_field02)
        major.save()

        self.assertEqual(major.name, name)
        self.assertEqual(list(major.fields.all()), [major_field01, major_field02])

        # testing name unique constrain
        self.assertRaises(IntegrityError, Major.objects.create, name=name)

    def test_delete_major(self):
        major01 = Major.objects.create(name="aTest Major")
        major02 = Major.objects.create(name="bTest Major")
        major03 = Major.objects.create(name="cTest Major")

        self.assertEqual(list(Major.objects.all()), [major01, major02, major03])

        major02.delete()

        self.assertEqual(list(Major.objects.all()), [major01, major03])

    def test_major_field_ordering(self):
        major01 = Major.objects.create(name="aTest Major Field")
        major03 = Major.objects.create(name="cTest Major Field")
        major02 = Major.objects.create(name="bTest Major Field")
        major05 = Major.objects.create(name="eTest Major Field")
        major04 = Major.objects.create(name="dTest Major Field")

        self.assertEqual(list(Major.objects.all()), [majord01, major02, major03, major04, major05])

    # MajorField model
    def test_create_major_field(self):
        major_field = MajorField.objects.create()
        self.assertIsInstance(major_field, MajorField)
        self.assertIsNone(major_field.name)

        name = "Engeneering"
        major_field.name = name
        major_field.save()

        self.assertEqual(major_field.name, name)

        # testing name unique constrain
        self.assertRaises(IntegrityError, MajorField.objects.create, name=name)

    def test_delete_major_field(self):
        major_field01 = MajorField.objects.create(name="aTest Major Field")
        major_field02 = MajorField.objects.create(name="bTest Major Field")
        major_field03 = MajorField.objects.create(name="cTest Major Field")

        self.assertEqual(list(MajorField.objects.all()), [major_field01, major_field02, major_field03])

        major_field02.delete()

        self.assertEqual(list(MajorField.objects.all()), [major_field01, major_field03])

    def test_major_field_ordering(self):
        major_field01 = MajorField.objects.create(name="aTest Major Field")
        major_field03 = MajorField.objects.create(name="cTest Major Field")
        major_field02 = MajorField.objects.create(name="bTest Major Field")
        major_field05 = MajorField.objects.create(name="eTest Major Field")
        major_field04 = MajorField.objects.create(name="dTest Major Field")

        self.assertEqual(
            list(MajorField.objects.all()), [major_field01, major_field02, major_field03, major_field04, major_field05]
        )

    # University model
    def test_create_university(self):
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        university = University.objects.create()
        self.assertIsInstance(university, University)
        self.assertIsNone(university.name)
        self.assertIsNone(university.cpnj)
        self.assertLessEqual(now_aware, university.created_at)
        self.assertLessEqual(now_aware, university.updated_at)

        name = "Test University"
        cnpj = "fake cnpj"
        university.name = name
        university.cnpj = cnpj
        university.save()

        self.assertEqual(university.name, name)
        self.assertEqual(university.cnpj, cnpj)

    def test_delete_university(self):
        university01 = University.objects.create(name="Test University")
        university02 = University.objects.create(name="Test University")
        university03 = University.objects.create(name="Test University")

        self.assertEqual(list(University.objects.all()), [university01, university02, university03])

        university02.delete()

        self.assertEqual(list(University.objects.all()), [university01, university03])

    def test_university_ordering(self):
        university01 = University.objects.create(name="aTest University")
        university03 = University.objects.create(name="cTest University")
        university02 = University.objects.create(name="bTest University")
        university05 = University.objects.create(name="eTest University")
        university04 = University.objects.create(name="dTest University")

        self.assertEqual(
            list(University.objects.all()), [university01, university02, university03, university04, university05]
        )
