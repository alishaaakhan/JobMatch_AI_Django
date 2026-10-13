from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from ml.predictor import predict_job_match
from .models import (
    Application,
    Job,
    JobMatch,
    SavedJob,
    Skill,
    UserProfile,
)

# ML predictor
from ml.predictor import predict_job_match


# ============================================================
# HOME
# ============================================================

def home(request):
    return render(
        request,
        "home.html"
    )


# ============================================================
# SIGN UP
# ============================================================

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # ----------------------------------------
        # Validate username
        # ----------------------------------------

        if not username:

            messages.error(
                request,
                "Username is required."
            )

            return redirect("signup")

        # ----------------------------------------
        # Validate password
        # ----------------------------------------

        if not password:

            messages.error(
                request,
                "Password is required."
            )

            return redirect("signup")

        # ----------------------------------------
        # Confirm password
        # ----------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("signup")

        # ----------------------------------------
        # Check existing username
        # ----------------------------------------

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("signup")

        # ----------------------------------------
        # Create Django User
        # ----------------------------------------

        user = User.objects.create_user(

            username=username,

            email=email,

            password=password
        )

        # ----------------------------------------
        # Create User Profile
        # ----------------------------------------

        UserProfile.objects.create(
            user=user
        )

        # ----------------------------------------
        # Login after signup
        # ----------------------------------------

        login(
            request,
            user
        )

        return redirect(
            "dashboard"
        )

    return render(
        request,
        "signup.html"
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect(
        "home"
    )


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def dashboard(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    saved_count = SavedJob.objects.filter(
        user=request.user
    ).count()

    application_count = Application.objects.filter(
        user=request.user
    ).count()

    match_count = JobMatch.objects.filter(
        user=request.user
    ).count()

    recent_jobs = Job.objects.filter(
        is_active=True
    ).order_by(
        "-created_at"
    )[:6]

    return render(
        request,
        "dashboard.html",
        {
            "profile": profile,
            "saved_count": saved_count,
            "application_count": application_count,
            "match_count": match_count,
            "recent_jobs": recent_jobs,
        }
    )


# ============================================================
# PROFILE
# ============================================================

@login_required(login_url="login")
def profile(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        # -----------------------------
        # Basic profile information
        # -----------------------------

        education = request.POST.get(
            "education",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        preferred_job_type = request.POST.get(
            "preferred_job_type",
            "Full Time"
        ).strip()

        # -----------------------------
        # Experience
        # -----------------------------

        experience_value = request.POST.get(
            "experience_years",
            "0"
        ).strip()

        try:
            experience_years = int(experience_value)

            if experience_years < 0:
                experience_years = 0

        except (ValueError, TypeError):

            experience_years = 0

        # -----------------------------
        # Save profile information
        # -----------------------------

        profile.education = education
        profile.experience_years = experience_years
        profile.location = location
        profile.preferred_job_type = preferred_job_type

        profile.save()

        # -----------------------------
        # Save Skills
        # -----------------------------

        skills_text = request.POST.get(
            "skills",
            ""
        ).strip()

        # Remove old skills first
        profile.skills.clear()

        if skills_text:

            # Example:
            # Python,C++,SQL,Django

            skill_names = skills_text.split(",")

            for skill_name in skill_names:

                skill_name = skill_name.strip()

                if not skill_name:
                    continue

                skill, created = Skill.objects.get_or_create(
                    name=skill_name
                )

                profile.skills.add(skill)

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
        }
    )


# ============================================================
# JOB LIST
# ============================================================

@login_required
def job_list(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    jobs = Job.objects.filter(
        is_active=True
    )

    if query:

        jobs = jobs.filter(
            title__icontains=query
        ) | jobs.filter(
            company__icontains=query
        ) | jobs.filter(
            category__icontains=query
        )

    jobs = jobs.distinct()

    return render(
        request,
        "jobs.html",
        {
            "jobs": jobs,
            "query": query,
        }
    )


# ============================================================
# JOB DETAIL
# ============================================================

@login_required
def job_detail(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    saved = SavedJob.objects.filter(
        user=request.user,
        job=job
    ).exists()

    applied = Application.objects.filter(
        user=request.user,
        job=job
    ).exists()

    return render(
        request,
        "job_detail.html",
        {
            "job": job,
            "saved": saved,
            "applied": applied,
        }
    )


# ============================================================
# SAVE JOB
# ============================================================

@login_required
def save_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    saved, created = SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )

    if created:

        messages.success(
            request,
            "Job saved successfully."
        )

    else:

        saved.delete()

        messages.info(
            request,
            "Job removed from saved jobs."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "job_list"
        )
    )


# ============================================================
# APPLY JOB
# ============================================================

@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    Application.objects.get_or_create(
        user=request.user,
        job=job
    )

    messages.success(
        request,
        "Application recorded successfully."
    )

    return redirect(
        "job_detail",
        job_id=job.id
    )


# ============================================================
# SAVED JOBS
# ============================================================

@login_required
def saved_jobs(request):

    saved = SavedJob.objects.filter(
        user=request.user
    ).select_related(
        "job"
    )

    return render(
        request,
        "saved_jobs.html",
        {
            "saved_jobs": saved,
        }
    )


# ============================================================
# APPLICATIONS
# ============================================================

@login_required
def applications(request):

    application_list = Application.objects.filter(
        user=request.user
    ).select_related(
        "job"
    )

    return render(
        request,
        "applications.html",
        {
            "applications": application_list,
        }
    )


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

@login_required
def recommendations(request):

    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    jobs = Job.objects.filter(
        is_active=True
    )

    recommendations_list = []

    for job in jobs:

        try:

            result = predict_job_match(
                profile,
                job
            )

            recommendations_list.append(
                {
                    "job": job,

                    "score":
                        result["match_score"],

                    "matched":
                        result["matched_skills"],

                    "missing":
                        result["missing_skills"],

                    "skill_overlap":
                        result["skill_overlap"],

                    "experience_fit":
                        result["experience_fit"],

                    "education_fit":
                        result["education_fit"],

                    "location_fit":
                        result["location_fit"],
                }
            )

        except Exception as e:

            print(
                f"ML prediction error for Job {job.id}: {e}"
            )

    recommendations_list.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return render(
        request,
        "recommendations.html",
        {
            "recommendations":
                recommendations_list[:20]
        }
    )