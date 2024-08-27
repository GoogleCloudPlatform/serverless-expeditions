# Gemini Python Django Application

This section contains source code for the Python Django application.

 - Python 3.12 + Django

## Build and Deploy to Google Cloud Run

### Requirements

#### Google Cloud CLI

 - [Google Cloud CLI](https://cloud.google.com/cli). Tested with version 470 (2024-04-26).

#### Google Gemini API Key

 - [Google Gemini API Key](https://aistudio.google.com/app/prompts/new_chat/).

#### Google Cloud Secrets Manager

 - The application reads the Google Gemini API Key in Google Secrets Manager. The secret name is **GEMINI_API_KEY**.
 - TODO: Publish my tool to create and rotate the secret.

#### Google Cloud Run Permissions
 - The service account attached to Google Cloud reads the secret from Google Secrets Manager. Add the role **Secret Manager Secret Accessor** to the project's IAM for the service account.
 - TODO: Pubish my tools to modify IAM permissions

Operating System Specific Instructions:
 - [Docker](BUILD_DOCKER.md)
 - [Linux](BUILD_LINUX.md)
 - [Windows](BUILD_WINDOWS.md)
