### Testing on Linux

 - This application is tested with Python 3.12.
 - From this directory create a Python virtual environment:

    - **python -m venv venv**
    - **venv/Scripts/activate.sh**

 - Install dependencies
    - **python -m pip install -r requirements.txt**

 - Set the environment variable **GCP_PROJECT_ID** to the Google Cloud Project.
    - Example: `export GCP_PROJECT_ID=myproject-123456`.

 - Configure Google Cloud Secrets Manager with your Google Gemini API Key.

 - Run the application
    - **python manage.py runserver**

 - Launch a web browser and connect to **http://localhost:8080/**

### Linux Tools for Google Cloud

The **tools/linux** directory contains shell scripts to build and deploy to Google Cloud Run:

- **gcp_build.sh** - Builds the container using Google Cloud Build to Google Artifact Registry.
- **gcp_deploy.sh** - Deploys the container from Google Artifact Registry to Google Cloud Run.
- **gcp_check_build_upload.sh** - Output a list of files that will be upload to Google Cloud Buil. Run this command to make sure only required files are uploaded. Runs the command **gcloud meta list-files-for-upload**.

Review both files and make any desired changes to the region, location, repository, etc. The changes must match in both files.

    REGION=us-central1
    SERVICE_NAME=gemini-python-django-v0
    IMAGE_NAME=gemini-python-django-v0
    LOCATION=us-central1
    REPOSITORY=gemini-project

### Build and Deploy from Linux or WSL
1. OPTIONAL. From this directory execute `source ./add_tools.sh`. This adds the **tools/linux** directory to the PATH. The alternate is to specify the build tool using the syntax **tools/windows/TOOLNAME**.

    - Example: **./tools/linux/gcp_build.sh**
2. Set the environment variable **GCP_PROJECT_ID** to the Google Cloud Project.

    - Example: `export GCP_PROJECT_ID=myproject-123456`.
3. Verify the list of files to be included in the container image:
    - gcp_check_build_upload.sh**
4. To build the container execute:
    - **gcp_build.sh**
5. To deploy the container to Cloud Run execute:
    - **gcp_deploy.sh**
