from django.contrib import admin

from .models import (
    Application,
    Job,
    JobMatch,
    JobSkill,
    SavedJob,
    Skill,
    UserProfile,
)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "category",
        "location",
        "job_type",
        "salary_inr",
        "is_active",
    )

    list_filter = (
        "category",
        "job_type",
        "location",
        "is_active",
    )

    search_fields = (
        "title",
        "company",
        "category",
        "location",
    )

    inlines = [JobSkillInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "education",
        "experience_years",
        "location",
        "preferred_job_type",
    )

    list_filter = (
        "education",
        "preferred_job_type",
    )

    search_fields = (
        "user__username",
        "user__email",
        "location",
    )


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "saved_at",
    )

    search_fields = (
        "user__username",
        "job__title",
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "status",
        "applied_at",
    )

    list_filter = ("status",)

    search_fields = (
        "user__username",
        "job__title",
    )


@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "match_score",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "user__username",
        "job__title",
    )


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = (
        "job",
        "skill",
        "required",
    )

    list_filter = ("required",)

    search_fields = (
        "job__title",
        "skill__name",
    )