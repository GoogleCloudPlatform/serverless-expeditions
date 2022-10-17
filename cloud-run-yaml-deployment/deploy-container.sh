AR_REGION=us-central1
PROJECT_ID=  # YOUR GCP PROJECT ID GOES HERE
AR_REPO_URL=$AR_REGION-docker.pkg.dev/$PROJECT_ID/my-serverless-app

gcloud run deploy app \
  --image $AR_REPO_URL/website \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --update-env-vars CITY=London \
  --project $PROJECT_ID