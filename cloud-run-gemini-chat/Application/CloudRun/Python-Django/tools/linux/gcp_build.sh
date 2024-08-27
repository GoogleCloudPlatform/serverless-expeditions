#!/bin/bash

if [[ -z "${GCP_PROJECT_ID}" ]];
then
	echo Please define the environment variable GCP_PROJECT_ID
	exit 1
fi

# GCP_PROJECT_ID=
REGION=us-central1
SERVICE_NAME=gemini-python-django-v0
IMAGE_NAME=gemini-python-django-v0
LOCATION=us-central1
REPOSITORY=gemini-project

echo Building image $LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$REPOSITORY/$IMAGE_NAME

gcloud builds submit \
--tag $LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$REPOSITORY/$IMAGE_NAME
RET=$?

if [ $RET -eq 0 ];
then
	exit 0
fi

echo "***************************************************************"
echo "Build Failed     Build Failed     Build Failed     Build Failed"
echo "***************************************************************"

exit 0
