# Hello Django, Cloud Run, Terraform

## Video guide

This source code accompanies the
[Serverless Expeditions: How to set up Django on Cloud Run with Terraform](https://www.youtube.com/watch?v=scdtpMBLT8A)
video.

## Provisioning, Migrations, and Deployment

1. Create project with billing enabled, and configure gcloud for that project

   ```
   PROJECT_ID=foobar
   gcloud config set project $PROJECT_ID
   ```

1. Configure default credentials (allows Terraform to apply changes):

   ```
   gcloud auth application-default login
   ```

1. Enable base services:

   ```
   gcloud services enable \
     cloudbuild.googleapis.com \
     run.googleapis.com \
     cloudresourcemanager.googleapis.com
   ```

1. Build base image

   ```
   gcloud builds submit
   ```

1. Apply Terraform

   ```
   terraform init
   terraform apply -var project=$PROJECT_ID
   ```

1. Run database migrations

   ```
   gcloud builds submit --config cloudbuild-migrate.yaml
   ```

1. Open service, getting the URL and password from the Terraform output:

   ```
   terraform output service_url
   terraform output superuser_password
   ```

## Local development

After deploying elements:

1. Install Cloud SQL Auth Proxy and run in a separate process. Generate the command from terraform output:
   ```
   terraform output -raw cloud_sql_proxy
   ```
1. TODO get settings file locally.
1. Setup Python environment and install dependencies
   ```
   virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
1. Set the local flag to have Django recognise local Proxy, then run service

   ```
   USE_CLOUD_SQL_AUTH_PROXY=true python manage.py runserver
   ```

## Files

Django website source

- `manage.py`, `gametracker/`, `requirements.txt`
  - Generated from `django-admin startproject` command

Manual edits:

- `gametracker/settings.py` updated to use `django-environ` and `django-storages`, pull secret settings
- Custom migration in `gametracker/migrations` to create superuser programatically as a data migration
- Basic models, views, and templates added.
- App presumes data entry from admin, displayed on website.

Deployment:

- `cloudbuild.yaml`
  - create base container image
- `main.tf`
  - one file for all Terraform config
- `etc/`
  - `env.tpl`: template file to help create the django settings file
- `cloudbuild-migrate.yaml`
  - django database migrations
