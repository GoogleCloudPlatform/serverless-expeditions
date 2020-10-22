export SERVICE_NAME=dbt-test
gcloud run deploy ${SERVICE_NAME} \
    --image gcr.io/$(gcloud config get-value project)/${SERVICE_NAME} \
    --allow-unauthenticated \
    --platform managed \
    --region us-central1
