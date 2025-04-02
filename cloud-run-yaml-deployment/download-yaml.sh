PROJECT_ID=

gcloud run services describe app --format export \
    --region us-central1 \
    --project $PROJECT_ID > service.yaml
