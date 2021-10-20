This Cloud Run service demonstrates how to run a shell script in the cloud.
It does so by running a Firestore backup operation when the Cloud Run services's
URL is accessed. Replace the contents on script.sh with whatever shell script
you need to run in the cloud.

1. Create a bucket in Google Cloud Storage (or reuse an existing one). The
Firestore backups will be written to this bucket.
1. Enter the name of that bucket in script.sh.
1. Grant these permissions to the service account that executes the Cloud Run
service. The default account will be xxxxxxxxxxxx-compute@developer.gserviceaccount.com
also known as the "Default compute service account".
    * Cloud Datastore Import Export Admin.
    * Storage Admin, for the Cloud Storage bucket. (If you are using the "Default compute service account", no need to add this permission. It already has it.)
1. Enter your Google Cloud project ID in deploy.sh/deploy.bat.
1. Run deploy.sh/deploy.bat to deploy the Cloud Run service.
