from django.urls import path

from . import views


urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # User
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),

    # Jobs
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),

    # Job actions
    path(
        "jobs/<int:job_id>/save/",
        views.save_job,
        name="save_job"
    ),

    path(
        "jobs/<int:job_id>/apply/",
        views.apply_job,
        name="apply_job"
    ),

    # User job sections
    path(
        "recommendations/",
        views.recommendations,
        name="recommendations"
    ),

    path(
        "saved-jobs/",
        views.saved_jobs,
        name="saved_jobs"
    ),

    path(
        "applications/",
        views.applications,
        name="applications"
    ),
]