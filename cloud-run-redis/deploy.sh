GOOGLE_PROJECT_ID=
SERVICE_NAME=
REDIS_HOST=
REDIS_PORT=
VPC_CONNECTOR=

gcloud beta run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --update-env-vars REDIS_HOST=$REDIS_HOST,REDIS_PORT=$REDIS_PORT \
  --vpc-connector $VPC_CONNECTOR \
  --project=$GOOGLE_PROJECT_ID
