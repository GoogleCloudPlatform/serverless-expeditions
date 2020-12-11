# Deploy to Cloud Run

```sh
GCP_PROJECT=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
gcloud builds submit --tag gcr.io/$GCP_PROJECT/myapp
gcloud run deploy myapp --image gcr.io/$GCP_PROJECT/myapp
```

With config:

```sh
GCP_PROJECT=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
gcloud builds submit --tag gcr.io/$GCP_PROJECT/myapp
gcloud run deploy myapp --image gcr.io/$GCP_PROJECT/myapp --platform managed --allow-unauthenticated
```