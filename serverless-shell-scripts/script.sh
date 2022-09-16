# Replace [BUCKET NAME] below with the name of your Google Cloud Storage bucket.
set -e
gcloud firestore export gs://[BUCKET NAME] --async
echo All done!