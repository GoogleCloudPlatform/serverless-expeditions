### Testing on Windows

 - This application is tested with Python 3.12.
 - From this directory create a Python virtual environment:

    - **python -m venv venv**
    - **venv\Scripts\activate.bat**

 - Install dependencies
    - **python -m pip install -r requirements.txt**

 - Set the environment variable **GCP_PROJECT_ID** to the Google Cloud Project.
    - Example: `set GCP_PROJECT_ID=myproject-123456`.

 - Configure Google Cloud Secrets Manager with your Google Gemini API Key.

 - Run the application
    - **python manage.py runserver**

 - Launch a web browser and connect to **http://localhost:8080/**

### Windows Tools for Google Cloud

The **tools\windows** directory contains batch files to build and deploy to Google Cloud Run:

- **gcp_build.bat** - Builds the container using Google Cloud Build to Google Artifact Registry.
- **gcp_deploy.bat** - Deploys the container from Google Artifact Registry to Google Cloud Run.
- **gcp_check_build_upload.bat** - Output a list of files that will be upload to Google Cloud Buil. Run this command to make sure only required files are uploaded. Runs the command **gcloud meta list-files-for-upload**.

Review both files and make any desired changes to the region, location, repository, etc. The changes must match in both files.

    @set REGION=us-central1
    @set SERVICE_NAME=gemini-python-django-v0
    @set IMAGE_NAME=gemini-python-django-v0
    @set LOCATION=us-central1
    @set REPOSITORY=gemini-project

### Build and Deploy from Windows
1. OPTIONAL. From this directory execute `add_tools.bat`. This adds the **tools\windows** directory to the PATH. The alternate is to specify the build tool using the syntax **tools\windows\TOOLNAME**.

    - Example: **.\tools\windows\gcp_build.bat**
2. Set the environment variable **GCP_PROJECT_ID** to the Google Cloud Project.

    - Example: `set GCP_PROJECT_ID=myproject-123456`.
3. Verify the list of files to be included in the container image:
    - gcp_check_build_upload.bat**
4. To build the container execute:
    - **gcp_build.bat**
5. To deploy the container to Cloud Run execute:
    - **gcp_deploy.bat**
