PROJECT_ID=

gcloud builds submit \
  --tag gcr.io/$PROJECT_ID/app \
  --project $PROJECT_ID
