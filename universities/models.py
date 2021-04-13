from django.db import models


class University(models.Model):
    """
    University table
    """

    name = models.CharField(max_length=50, blank=True, null=True)
    cpnj = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class MajorField(models.Model):
    """
    Major field table - study field of a major, can be broad or specific
    e.g., Engeneering, Science, Politics, Health, etc
    """

    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Major(models.Model):
    """
    Major table - undergraduation course
    e.g., Computer Engeneering, Economics, Law, etc
    """

    name = models.CharField(max_length=50, blank=True, null=True)
    fields = models.ManyToManyField(MajorField, related_name="majors")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
