import os

import joblib


# ============================================================
# LOAD MODEL
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "job_match_model.pkl"
)

model_data = joblib.load(
    MODEL_PATH
)

model = model_data["model"]

FEATURE_NAMES = model_data[
    "feature_names"
]


# ============================================================
# PREDICT JOB MATCH
# ============================================================

def predict_job_match(
    user_profile,
    job
):

    # --------------------------------------------------------
    # Candidate skills
    # --------------------------------------------------------

    candidate_skills = set(
        skill.name.lower().strip()
        for skill in user_profile.skills.all()
    )

    # --------------------------------------------------------
    # Job skills
    # --------------------------------------------------------

    job_skills = set(
        skill.name.lower().strip()
        for skill in job.skills.all()
    )

    # --------------------------------------------------------
    # Matched / missing skills
    # --------------------------------------------------------

    matched_skills = (
        candidate_skills.intersection(
            job_skills
        )
    )

    missing_skills = (
        job_skills.difference(
            candidate_skills
        )
    )

    candidate_skill_count = len(
        candidate_skills
    )

    job_skill_count = len(
        job_skills
    )

    matched_skill_count = len(
        matched_skills
    )

    # --------------------------------------------------------
    # Skill overlap
    # --------------------------------------------------------

    if job_skill_count > 0:

        skill_overlap = (
            matched_skill_count
            /
            job_skill_count
        )

    else:

        skill_overlap = 0

    # --------------------------------------------------------
    # Jaccard similarity
    # --------------------------------------------------------

    union_count = len(
        candidate_skills.union(
            job_skills
        )
    )

    if union_count > 0:

        jaccard = (
            matched_skill_count
            /
            union_count
        )

    else:

        jaccard = 0

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    candidate_experience = (
        user_profile.experience_years
    )

    job_experience = (
        job.experience_years
    )

    experience_gap = (
        candidate_experience
        -
        job_experience
    )

    if candidate_experience >= job_experience:

        experience_fit = 1

    elif candidate_experience + 1 >= job_experience:

        experience_fit = 0.5

    else:

        experience_fit = 0

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    candidate_education = (
        user_profile.education
    )

    job_education = (
        job.education
    )

    education_fit = int(

        candidate_education
        ==
        job_education

        or

        not job_education

        or

        job_education == "Other"
    )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    candidate_location = (
        user_profile.location
    )

    job_location = (
        job.location
    )

    candidate_location_lower = (
        candidate_location.lower().strip()
    )

    job_location_lower = (
        job_location.lower().strip()
    )

    location_fit = int(

        candidate_location_lower
        ==
        job_location_lower

        or

        candidate_location_lower
        ==
        "remote"

        or

        job_location_lower
        ==
        "remote"
    )

    # --------------------------------------------------------
    # Job type
    # --------------------------------------------------------

    is_internship = int(
        job.job_type == "Internship"
    )

    is_full_time = int(
        job.job_type == "Full Time"
    )

    is_contract = int(
        job.job_type == "Contract"
    )

    # --------------------------------------------------------
    # ML features
    # --------------------------------------------------------

    features = [[

        skill_overlap,

        jaccard,

        matched_skill_count,

        candidate_skill_count,

        job_skill_count,

        candidate_experience,

        job_experience,

        experience_gap,

        experience_fit,

        education_fit,

        location_fit,

        is_internship,

        is_full_time,

        is_contract,

    ]]

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        features
    )[0]

    match_probability = probabilities[1]

    match_score = round(
        match_probability * 100,
        2
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {

        "match_score":
            match_score,

        "matched_skills":
            sorted(matched_skills),

        "missing_skills":
            sorted(missing_skills),

        "skill_overlap":
            round(
                skill_overlap * 100,
                2
            ),

        "experience_fit":
            experience_fit,

        "education_fit":
            education_fit,

        "location_fit":
            location_fit,
    }