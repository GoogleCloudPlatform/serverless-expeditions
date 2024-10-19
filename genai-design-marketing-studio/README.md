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
 
- A folder named `prompts` contains a single json file containing the different prompts used by Gemini and Imagen3. You can edit this JSON file before deploying the application (permanent change), or modify the prompts directly from the application (changes are lost when the application is closed).

- The files needed to build the application with Google Builds

  - the very standard `Dockerfile`
  - the `cloudbuild.yaml` which is used by the Google Cloud Builds service
  - the `requirements.txt` which contains the libraries used by the application, notice how short it is.


  
