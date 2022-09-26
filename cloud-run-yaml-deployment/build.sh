AR_REGION=us-central1
PROJECT_ID=  # YOUR GCP PROJECT ID GOES HERE
AR_REPO_URL=$REGION-docker.pkg.dev/$PROJECT_ID/my-serverless-app  

gcloud builds submit \
  --tag $AR_REPO_URL/website \
  --project $PROJECT_ID
