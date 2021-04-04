# Setup
gcloud auth revoke
kill -9 $(lsof -t -i:8080)

# Login
gcloud auth login
GOOGLE_PROJECT_ID=critterwatcher

# Local debug
npm start

# Local debug – ADC 
gcloud auth application-default login
GOOGLE_CLOUD_PROJECT=critterwatcher npm start

# Deploy
gcloud functions deploy critterwatch-function \
  --project=critterwatcher \
  --trigger-http \
  --runtime nodejs12