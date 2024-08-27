#!/bin/bash

GCP_PROJECT_ID=jobs-long-running
REGION=us-central1
SERVICE_NAME=gemini-python-flask-v0
LOCATION=us-central1

gcloud run deploy $SERVICE_NAME \
	--source . \
	--region $REGION \
	--allow-unauthenticated \
	--platform managed
