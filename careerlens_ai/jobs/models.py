from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):

    EDUCATION_CHOICES = [
        ("B.Tech", "B.Tech"),
        ("BCA", "BCA"),
        ("MCA", "MCA"),
        ("M.Tech", "M.Tech"),
        ("B.Sc", "B.Sc"),
        ("M.Sc", "M.Sc"),
        ("BBA", "BBA"),
        ("MBA", "MBA"),
        ("B.Des", "B.Des"),
        ("BA", "BA"),
        ("Other", "Other"),
    ]

    JOB_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    education = models.CharField(
        max_length=50,
        choices=EDUCATION_CHOICES,
        blank=True
    )

    experience_years = models.PositiveIntegerField(default=0)

    location = models.CharField(
        max_length=100,
        blank=True
    )

    preferred_job_type = models.CharField(
        max_length=30,
        choices=JOB_TYPE_CHOICES,
        default="Full Time"
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="users"
    )

    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ("Full Time", "Full Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    ]

    title = models.CharField(max_length=200)

    company = models.CharField(max_length=200)

    description = models.TextField()

    education = models.CharField(
        max_length=100,
        blank=True
    )

    experience_years = models.PositiveIntegerField(default=0)

    location = models.CharField(max_length=100)

    state = models.CharField(
        max_length=100,
        blank=True
    )

    category = models.CharField(max_length=100)

    salary_inr = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    job_type = models.CharField(
        max_length=30,
        choices=JOB_TYPE_CHOICES
    )

    skills = models.ManyToManyField(
        Skill,
        through="JobSkill",
        related_name="jobs"
    )

    application_url = models.URLField(
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


class JobSkill(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    required = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job.title} - {self.skill.name}"

    class Meta:
        unique_together = ("job", "skill")


class SavedJob(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="saved_jobs"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="saved_by"
    )

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class Application(models.Model):

    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Shortlisted", "Shortlisted"),
        ("Interview", "Interview"),
        ("Rejected", "Rejected"),
        ("Selected", "Selected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class JobMatch(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_matches"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="matches"
    )

    match_score = models.FloatField()

    matched_skills = models.TextField(
        blank=True
    )

    missing_skills = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.job.title} - {self.match_score}%"