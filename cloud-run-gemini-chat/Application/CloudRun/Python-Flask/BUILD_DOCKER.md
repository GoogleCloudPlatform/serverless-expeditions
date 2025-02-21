### Build and Run locally with Docker
TODO: Publish my Docker container build and run tools.

TODO: Publish my Docker tools

### Example command to build the container:

 - **docker build -t gemini-python-flask .**

### Example script to run the container (Docker on Windows):

 - Notice some of the options to use a service account inside the container. On my system, I keep secrets, services accounts, etc in a special directory. This command is setup for development and testing.

```
@if not defined GCP_PROJECT_ID (
	@echo Please define the environment variable GCP_PROJECT_ID
	Exit /B 1
)

docker run -it --rm --name gemini-python-flask ^
-p 8080:8080 ^
-v %cd%:/work ^
-v %APPDATA%\gcloud:/root/.config ^
-v c:/config:/config ^
-e GOOGLE_APPLICATION_CREDENTIALS=/config/service-account.json ^
-e GCP_PROJECT_ID=%GCP_PROJECT_ID% ^
-e FLASK_DEBUG=True ^
gemini-python-flask
```
