import pandas as pd

from django.conf import settings
from django.core.management.base import BaseCommand

from jobs.models import Job, Skill, JobSkill


class Command(BaseCommand):

    help = "Import jobs from jobs_dataset.csv"

    def handle(self, *args, **options):

        csv_path = (
            settings.BASE_DIR
            / "ml"
            / "dataset"
            / "jobs_dataset.csv"
        )

        self.stdout.write(
            f"Reading dataset from: {csv_path}"
        )

        try:

            df = pd.read_csv(csv_path)

        except FileNotFoundError:

            self.stdout.write(
                self.style.ERROR(
                    "jobs_dataset.csv was not found."
                )
            )

            return

        self.stdout.write(
            f"Found {len(df)} jobs in dataset."
        )

        imported = 0

        for _, row in df.iterrows():

            # -----------------------------
            # Job information
            # -----------------------------

            job_id = int(row["job_id"])

            title = str(
                row["job_title"]
            ).strip()

            company = str(
                row["company"]
            ).strip()

            education = str(
                row["education"]
            ).strip()

            location = str(
                row["location"]
            ).strip()

            state = str(
                row["state"]
            ).strip()

            category = str(
                row["category"]
            ).strip()

            job_type = str(
                row["job_type"]
            ).strip()

            experience_years = int(
                row["experience_years"]
            )

            # Salary
            salary_value = row["salary_inr"]

            if pd.isna(salary_value):
                salary_inr = None
            else:
                salary_inr = int(
                    salary_value
                )

            # Skills
            skills_text = str(
                row["skills"]
            ).strip()

            description = (
                f"{title} opportunity at {company}. "
                f"This role belongs to the {category} "
                f"category and is based in {location}. "
                f"The position requires {experience_years} "
                f"years of experience and skills including "
                f"{skills_text}."
            )

            # -----------------------------
            # Create / update Job
            # -----------------------------

            job, created = Job.objects.update_or_create(

                id=job_id,

                defaults={
                    "title": title,
                    "company": company,
                    "description": description,
                    "education": education,
                    "experience_years": experience_years,
                    "location": location,
                    "state": state,
                    "category": category,
                    "salary_inr": salary_inr,
                    "job_type": job_type,
                    "is_active": True,
                }
            )

            # -----------------------------
            # Job Skills
            # -----------------------------

            # Remove old skill relationships
            JobSkill.objects.filter(
                job=job
            ).delete()

            skill_names = skills_text.split(",")

            for skill_name in skill_names:

                skill_name = skill_name.strip()

                if not skill_name:
                    continue

                skill, _ = Skill.objects.get_or_create(
                    name=skill_name
                )

                JobSkill.objects.create(
                    job=job,
                    skill=skill,
                    required=True
                )

            imported += 1

            if imported % 100 == 0:

                self.stdout.write(
                    f"Imported {imported} jobs..."
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully imported {imported} jobs."
            )
        )