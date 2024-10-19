# GenAI Design and Marketing Studio Application
### Designed by Google WSSV GenAI FSA team 
#### contact: jeromemassot@google.com
#### October 2024

This folder contains the source code for the Generative AI Design and Marketing Studio application.

## What is this repository about?

The code that you can find in this repository will allow you to create a Design and Marketing Studio where different GenAI assistants will help you in your daily Design and Marketing activities.

## Repository Organization

The repository contains all the code needed to deploy the Design and Marketing platform in your Google Cloud Project.

- Two Python files contain the generative engine and the user interface (made with Streamlit):

  - `generative.py`: contains all the Generative AI code using the Vertex AI API (Gemini and Imagen3). You can see that the file is concise. It is the main advantage of using the Google Vertex AI APIs where all the long and difficult codes have already been written and tested by the Google teams, and run on the server side (in a serverless manner).
 
  - `streamlit_app.py`: contains all the code needed to create the Streamlit application. Altogether, this quite rich application is made with only ~700 lines of Python.
 
- A folder named `.streamlit` contains a single `config.toml` file containing the parameters used to run the Streamlit server on Google Cloud.
 
- A folder named `prompts` contains a single JSON file containing the different prompts used by Gemini and Imagen3. You can edit this JSON file before deploying the application (permanent change), or modify the prompts directly from the application (changes are lost when the application is closed).

- The files needed to build the application with Google Builds

  - the very standard `Dockerfile`
  - the `cloudbuild.yaml` used by the Google Cloud Builds service. You must adapt this file to your configuration.
  - the `requirements.txt` which contains the libraries used by the application, notice how short it is.

### How do you deploy the application on Google Cloud?

The easiest way to deploy this application on your Google Cloud project is to:
- build the image using the Docker file with Cloud Build and store it in your Artifact Repository
- deploy the service using Cloud Run and the image stored in the Artifact Repository
- if you want to restrict access to the service, the easiest way is to use the automatic integration tool available with Cloud Run

## How do you use this Design and Marketing Studio?
A short documentation is provided in the repository.
