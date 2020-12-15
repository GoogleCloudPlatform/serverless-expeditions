# Gcloud Tips and Tricks

Tips and tricks when using `gcloud`.

## Setup

```sh
PROJECT=$(gcloud config get-value project)
PROJECT_ID=$PROJECT
cd myapp && gcloud builds submit --tag gcr.io/$PROJECT/helloworld && cd ..
gcloud config unset run/platform
gcloud config unset run/region
```

## Tips

```sh
# Tip 1: Interactive Mode
gcloud beta interactive

gcloud run deploy --













# Tip 2: Prevent Prompts. Set Defaults.

gcloud config set <property> <value>

## Without flags

## Flags
gcloud run deploy myapp \
  --image gcr.io/$PROJECT/myapp \
  --platform managed \
  --region europe-west3

## Or config
gcloud config set run/platform managed
gcloud config set run/region europe-west3

gcloud run deploy myapp \
  --image gcr.io/$PROJECT/myapp







# Tip 3: Getting / Setting Project ID
gcloud config set project "my-project"
PROJECT=$(gcloud config get-value core/project)













# Tip 4: See if Billing Is Enabled
gcloud beta billing projects describe \
  $(gcloud config get-value project) \
  --format="value(billingEnabled)"













# Tip 5: Authenticated Test Cloud Run
gcloud run deploy myapp \
  --image gcr.io/$PROJECT/myapp

curl https://myapp-q7vieseilq-ey.a.run.app

curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
https://myapp-q7vieseilq-ey.a.run.app










# Tips 6: Project ID To Project Number
PROJECT_NUMBER=$(gcloud projects list \
  --filter="project_id:$PROJECT_ID" \
  --format='value(project_number)')
echo $PROJECT_NUMBER

PROJECT_ID=$(gcloud projects list \
  --filter="$PROJECT_NUMBER" \
  --format="value(project_id)")
echo $PROJECT_ID

# Cloud Run uses Compute Engine default service account
SERVICE_ACCOUNT=$PROJECT_NUMBER-compute@developer.gserviceaccount.com
echo $SERVICE_ACCOUNT

gcloud run services update myapp --service-account $SERVICE_ACCOUNT
```
