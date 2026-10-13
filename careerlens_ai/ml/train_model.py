import os
import random

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

DATASET_PATH = os.path.join(
    DATASET_DIR,
    "candidate_job_training.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "job_match_model.pkl"
)


# ============================================================
# RANDOM SEED
# ============================================================

random.seed(42)
np.random.seed(42)


# ============================================================
# CREATE TRAINING DATASET
# ============================================================

def create_dataset():

    os.makedirs(
        DATASET_DIR,
        exist_ok=True
    )

    skills_list = [
        "Python",
        "Java",
        "C++",
        "C",
        "JavaScript",
        "React",
        "Django",
        "Flask",
        "HTML",
        "CSS",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Power BI",
        "Tableau",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "Data Analysis",
        "Data Science",
        "AWS",
        "Azure",
        "Docker",
        "Git",
        "GitHub",
        "Flutter",
        "Dart",
        "Node.js",
        "Express.js",
        "Figma",
        "Excel",
        "Communication",
    ]

    job_titles = [
        "Python Developer",
        "Data Analyst",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
        "Web Developer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Software Developer",
        "Django Developer",
        "React Developer",
        "Business Analyst",
        "Power BI Developer",
        "Junior Data Scientist",
        "ML Intern",
        "Python Intern",
        "Software Engineering Intern",
        "Data Analyst Intern",
        "AI/ML Intern",
    ]

    education_options = [
        "B.Tech",
        "BCA",
        "MCA",
        "M.Tech",
        "B.Sc",
        "M.Sc",
        "BBA",
        "MBA",
        "BA",
        "Other",
    ]

    locations = [
        "Bhopal",
        "Indore",
        "Delhi",
        "Mumbai",
        "Pune",
        "Bangalore",
        "Hyderabad",
        "Chennai",
        "Noida",
        "Gurgaon",
        "Kolkata",
        "Ahmedabad",
        "Remote",
    ]

    job_types = [
        "Full Time",
        "Internship",
        "Contract",
    ]

    categories = [
        "Software Development",
        "Data Science",
        "Data Analytics",
        "Artificial Intelligence",
        "Web Development",
        "Business Analytics",
        "Cloud Computing",
    ]

    companies = [
        "TechNova Solutions",
        "DataSphere Labs",
        "InnoSoft Technologies",
        "CloudMatrix",
        "NextGen Analytics",
        "CodeCraft Technologies",
        "AIWorks India",
        "ByteBridge",
        "DigitalCore",
        "FutureTech Labs",
        "InsightEdge",
        "SmartStack Technologies",
    ]

    rows = []

    for i in range(2000):

        candidate_skill_count = random.randint(
            3,
            10
        )

        job_skill_count = random.randint(
            3,
            8
        )

        candidate_skills = set(
            random.sample(
                skills_list,
                candidate_skill_count
            )
        )

        job_skills = set(
            random.sample(
                skills_list,
                job_skill_count
            )
        )

        matched_skills = (
            candidate_skills.intersection(
                job_skills
            )
        )

        skill_overlap = (
            len(matched_skills)
            /
            len(job_skills)
        )

        jaccard = (
            len(
                candidate_skills.intersection(
                    job_skills
                )
            )
            /
            len(
                candidate_skills.union(
                    job_skills
                )
            )
        )

        candidate_experience = random.randint(
            0,
            7
        )

        job_experience = random.randint(
            0,
            5
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

        candidate_education = random.choice(
            education_options
        )

        job_education = random.choice(
            education_options
        )

        education_fit = int(
            candidate_education == job_education
            or job_education == "Other"
        )

        candidate_location = random.choice(
            locations
        )

        job_location = random.choice(
            locations
        )

        location_fit = int(
            candidate_location == job_location
            or candidate_location == "Remote"
            or job_location == "Remote"
        )

        job_type = random.choice(
            job_types
        )

        is_internship = int(
            job_type == "Internship"
        )

        is_full_time = int(
            job_type == "Full Time"
        )

        is_contract = int(
            job_type == "Contract"
        )

        score = (
            skill_overlap * 0.50
            + jaccard * 0.20
            + experience_fit * 0.10
            + education_fit * 0.10
            + location_fit * 0.10
        )

        score += random.uniform(
            -0.08,
            0.08
        )

        match = int(
            score >= 0.50
        )

        rows.append(
            {
                "candidate_skill_count":
                    len(candidate_skills),

                "job_skill_count":
                    len(job_skills),

                "matched_skill_count":
                    len(matched_skills),

                "skill_overlap":
                    skill_overlap,

                "jaccard":
                    jaccard,

                "candidate_experience":
                    candidate_experience,

                "job_experience":
                    job_experience,

                "experience_gap":
                    experience_gap,

                "experience_fit":
                    experience_fit,

                "education_fit":
                    education_fit,

                "location_fit":
                    location_fit,

                "is_internship":
                    is_internship,

                "is_full_time":
                    is_full_time,

                "is_contract":
                    is_contract,

                "candidate_education":
                    candidate_education,

                "job_education":
                    job_education,

                "candidate_location":
                    candidate_location,

                "job_location":
                    job_location,

                "job_type":
                    job_type,

                "job_title":
                    random.choice(job_titles),

                "company":
                    random.choice(companies),

                "category":
                    random.choice(categories),

                "match":
                    match,
            }
        )

    df = pd.DataFrame(rows)

    df.to_csv(
        DATASET_PATH,
        index=False
    )

    print("=" * 60)
    print("DATASET CREATED")
    print("=" * 60)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print(
        f"Saved to: {DATASET_PATH}"
    )

    print("\nMatch distribution:")

    print(
        df["match"].value_counts()
    )

    return df


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model(df):

    print("\n" + "=" * 60)
    print("TRAINING ML MODEL")
    print("=" * 60)

    feature_columns = [

        "skill_overlap",

        "jaccard",

        "matched_skill_count",

        "candidate_skill_count",

        "job_skill_count",

        "candidate_experience",

        "job_experience",

        "experience_gap",

        "experience_fit",

        "education_fit",

        "location_fit",

        "is_internship",

        "is_full_time",

        "is_contract",
    ]

    X = df[
        feature_columns
    ]

    y = df[
        "match"
    ]

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42,

        stratify=y
    )

    print(
        f"Training records: {len(X_train)}"
    )

    print(
        f"Testing records: {len(X_test)}"
    )

    model = RandomForestClassifier(

        n_estimators=250,

        max_depth=10,

        min_samples_leaf=2,

        random_state=42,

        class_weight="balanced"
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nModel Accuracy:")

    print(
        f"{accuracy * 100:.2f}%"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions
        )
    )

    model_data = {

        "model":
            model,

        "feature_names":
            feature_columns,

        "version":
            "1.0"
    }

    joblib.dump(
        model_data,
        MODEL_PATH
    )

    print("=" * 60)
    print("MODEL SAVED")
    print("=" * 60)

    print(
        f"File: {MODEL_PATH}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "\nCareerLens AI - ML Training"
    )

    print(
        "=" * 60
    )

    dataset = create_dataset()

    train_model(
        dataset
    )

    print(
        "\nTraining completed successfully."
    )