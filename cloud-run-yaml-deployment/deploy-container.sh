PROJECT_ID=

gcloud beta run deploy app \
  --image gcr.io/$PROJECT_ID/app \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --project $PROJECT_ID