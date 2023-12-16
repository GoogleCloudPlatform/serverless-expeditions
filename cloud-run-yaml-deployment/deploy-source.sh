PROJECT_ID=

gcloud run deploy app --source . \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --project $PROJECT_ID
