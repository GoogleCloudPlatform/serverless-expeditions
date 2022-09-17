PROJECT_ID=

gcloud run services describe app --format export \
    --project $PROJECT_ID > service.yaml