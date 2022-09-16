GOOGLE_PROJECT_ID=[YOUR GOOGLE PROJECT ID]

gcloud run deploy \
  --source . \
  --project $GOOGLE_PROJECT_ID \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  my-shell-script
