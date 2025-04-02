# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

GOOGLE_PROJECT_ID=[Your Google Cloud project ID, from console.cloud.google.com]
SERVICE_NAME=[The name of your Cloud Run service]
REDIS_HOST=[IP address of your Memorystore/Redis instance]
REDIS_PORT=[Port used by your Memorystore/Redis instance]

gcloud beta run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --network=default \
  --subnet=default \
  --network-tags=frontend \
  --vpc-egress=private-ranges-only \
  --update-env-vars REDIS_HOST=$REDIS_HOST,REDIS_PORT=$REDIS_PORT \
  --project=$GOOGLE_PROJECT_ID
