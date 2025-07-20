# GenAI Design and Marketing Studio Application
### Designed by Google WSSV GenAI FSA team 
#### contact: jeromemassot@google.com
#### July 2025

This folder contains the source code for the Generative AI Design and Marketing Studio application.

## What is this repository about?

The code that you can find in this repository will allow you to create a Design and Marketing Studio where different GenAI assistants will help you in your daily Design and Marketing activities.

## Repository Organization

The repository contains all the code needed to deploy the Design and Marketing platform in your Google Cloud Project.

- Two Python files contain the generative engine and the user interface (made with Streamlit):

  - `generative.py`: contains all the Generative AI code using the Vertex AI API (Gemini and Imagen3). You can see that the file is concise. It is the main advantage of using the Google Vertex AI APIs where all the long and difficult codes have already been written and tested by the Google teams, and run on the server side (in a serverless manner).
 
  - `streamlit_app.py`: contains all the code needed to create the Streamlit application. Altogether, this quite rich application is made with only ~600 lines of Python.
 
- A folder named `.streamlit` contains a single `config.toml` file containing the parameters used to run the Streamlit server on Google Cloud.
 
- A folder named `prompts` contains a single JSON file containing the different prompts used by Gemini and Imagen3. You can edit this JSON file before deploying the application (permanent change), or modify the prompts directly from the application (changes are lost when the application is closed).

- The files needed to build the application with Google Builds

  - the very standard `Dockerfile`
  - the `cloudbuild.yaml` used by the Google Cloud Builds service. You must adapt this file to your configuration.
  - the `requirements.txt` which contains the libraries used by the application, notice how short it is.

### How do you deploy the application on Google Cloud?

The easiest way to deploy this application on your Google Cloud project is to:
- [OPTIONAL] Build the image with Cloud Build using the Docker file  and store it in your Artifact Registry: to do so, from the main folder of the application (the one where the Dockerfile is located), just enter the following command `gcloud builds submit`. Of course, you first need to update the cloudbuild.yaml with your project id and the repository id that will store the container image.
  
- [DEPLOY FROM ARTIFACT REGISTRY] Deploy the service on Cloud Run, using Cloud Run UI and the image stored in the Artifact Repository. The user interface is straightforward. You can deploy the image on the default backend (no GPU needed), as Gemini runs all the Generative AI tasks on Vertex AI and Imagen endpoints.

- [DEPLOY DIRECTLY FROM THE SOURCE] Deploy the service on Cloud Run directly from the source (main folder) by using the following command: `gcloud run deploy genai-design-platform --source .`. The newly built container image is pushed to a repository in Artifact Registry named `cloud-run-source-deploy`. The command will ask about the location of the created artifact registry and some authorization confirmation.
  
- If you want to restrict access to the service, the easiest way is to use the automatic integration tool available with Cloud Run

## How do you use this Design and Marketing Studio?
A short documentation is provided in the repository.
