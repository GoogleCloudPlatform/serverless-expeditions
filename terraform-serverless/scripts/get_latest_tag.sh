#!/bin/bash

# WORKAROUND SCRIPT

# The Terraform Google provider (as of 3.53.0) provides no way to get
# information about images in the Container registry.

# If Terraform sees the "latest" tag, it takes no action, even if the latest
# image has changed since last run.

# So, manually retrieve the most recent fully qualified digest for the image.

# This will ensure that a service is only redeployed if the image has been updated
# This will require you to run 'gcloud builds submit', or similar, separately.

PROJECT=$1
IMAGE=$2

# deep JSON is invalid for terraform, so serve flat value
LATEST=$(gcloud container images describe gcr.io/${PROJECT}/${IMAGE}:latest  --format="value(image_summary.fully_qualified_digest)" | tr -d '\n')
echo "{\"image\": \"${LATEST}\"}"
