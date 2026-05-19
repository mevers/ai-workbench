# LinkedIn Extraction Schemas

Use these schemas as structured YAML targets. Omit fields that are irrelevant, and keep `null` values only when the field is useful to the requested extraction.

## Profile Schema

```yaml
source_type: linkedin_profile
person:
  full_name:
  headline:
  location:
  about:
current_role:
  title:
  company:
  start_date:
  location:
experience:
  - title:
    company:
    employment_type:
    location:
    start_date:
    end_date:
    duration:
    description:
    visible_skill_tags:
education:
  - school:
    degree:
    field:
    start_date:
    end_date:
licences_certifications:
  - name:
    issuer:
    issue_date:
    expiration_date:
skills:
  - name:
    evidence:
featured_or_projects:
  - title:
    description:
    url:
contact_or_links:
  - label:
    value:
not_present:
notes:
```

## Job Post Schema

```yaml
source_type: linkedin_job
job:
  title:
  company:
  location:
  workplace_type:
  employment_type:
  seniority_level:
  salary_or_compensation:
  posted_date:
  applicant_count:
  application_method:
company:
  industry:
  size:
  description:
requirements:
  must_have:
  preferred:
responsibilities:
benefits:
screening_or_application_questions:
work_authorisation_or_travel:
not_present:
notes:
```

## Normalisation Rules

- Keep original labels when they carry meaning, such as "Hybrid", "Contract", or "Easy Apply".
- Normalise dates only when the source is clear. Preserve original date strings in notes when exact dates are unavailable.
- Split requirements into `must_have` and `preferred` only when the post distinguishes them. Otherwise keep them in `must_have` or a general requirements list and note the ambiguity.
- For profile experience, preserve chronology as shown. Keep each entry as a full object with title, company, dates, location, duration, description, and visible skill tags when present. Do not reduce experience to a title-only list. Do not fill gaps unless the user provides additional evidence.
