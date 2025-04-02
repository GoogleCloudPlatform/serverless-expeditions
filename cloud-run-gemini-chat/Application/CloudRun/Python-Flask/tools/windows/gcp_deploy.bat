@if not defined GCP_PROJECT_ID (
	@echo Please define the environment variable GCP_PROJECT_ID
	Exit /B 1
)

:: @set GCP_PROJECT_ID=
@set REGION=us-central1
@set SERVICE_NAME=gemini-python-flask-v0
@set IMAGE_NAME=gemini-python-flask-v0
@set LOCATION=us-central1
@set REPOSITORY=gemini-project

call gcloud run deploy %SERVICE_NAME% ^
--region %REGION% ^
--image %LOCATION%-docker.pkg.dev/%GCP_PROJECT_ID%/%REPOSITORY%/%IMAGE_NAME% ^
--execution-environment=gen1 ^
--memory=256Mi ^
--allow-unauthenticated ^
--platform managed
@if errorlevel 1 goto err_out

goto end

:err_out
@echo ***************************************************************
@echo Deplopy Failed  Deplopy Failed  Deplopy Failed   Deplopy Failed
@echo ***************************************************************

:end
