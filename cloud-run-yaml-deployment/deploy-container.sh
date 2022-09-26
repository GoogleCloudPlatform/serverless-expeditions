AR_REGION=us-central1
PROJECT_ID=cloud-run-fafo-f241  # YOUR GCP PROJECT ID GOES HERE
AR_REPO_URL=$AR_REGION-docker.pkg.dev/$PROJECT_ID/my-serverless-app  

gcloud beta run deploy app \
  --image $AR_REPO_URL/website \
  --platform managed \
  --allow-unauthenticated \
  --region us-central1 \
  --project $PROJECT_ID