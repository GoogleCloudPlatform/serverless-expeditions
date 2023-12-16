# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SERVICE_NAME=
GCP_REGION=
GCP_PROJECT_ID=

gcloud run deploy $SERVICE_NAME \
  --source . \
  --allow-unauthenticated \
  --region $GCP_REGION \
  --project $GCP_PROJECT_ID
