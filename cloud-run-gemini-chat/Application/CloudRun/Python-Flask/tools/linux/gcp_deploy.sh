#!/bin/bash

if [[ -z "${GCP_PROJECT_ID}" ]];
then
	echo Please define the environment variable GCP_PROJECT_ID
	exit 1
fi

# GCP_PROJECT_ID=
REGION=us-central1
SERVICE_NAME=gemini-python-flask-v0
IMAGE_NAME=gemini-python-flask-v0
LOCATION=us-central1
REPOSITORY=gemini-project

echo Deploying image $LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$REPOSITORY/$IMAGE_NAME

gcloud run deploy $SERVICE_NAME \
--region $REGION \
--image $LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$REPOSITORY/$IMAGE_NAME \
--execution-environment=gen1 \
--memory=256Mi \
--allow-unauthenticated \
--platform managed
RET=$?

if [ $RET -eq 0 ];
then
	exit 0
fi

echo "***************************************************************"
echo "Deplopy Failed  Deplopy Failed  Deplopy Failed   Deplopy Failed"
echo "***************************************************************"

exit 0
