GOOGLE_PROJECT_ID=# YOUR GCP PROJECT ID GOES HERE

gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/barkbarkapi \
  --project=$GOOGLE_PROJECT_ID

gcloud beta run deploy barkbark-api \
  --image gcr.io/$GOOGLE_PROJECT_ID/barkbarkapi \
  --platform managed \
  --region us-central1 \
  --project=$GOOGLE_PROJECT_ID
