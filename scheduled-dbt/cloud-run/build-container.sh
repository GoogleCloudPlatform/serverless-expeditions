export SERVICE_NAME=dbt-test
gcloud builds submit \
  --tag gcr.io/$(gcloud config get-value project)/${SERVICE_NAME}
