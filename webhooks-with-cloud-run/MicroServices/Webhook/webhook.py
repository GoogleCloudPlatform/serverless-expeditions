# Copyright 2019 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import hmac
import json
import os
import sys
import time
import urllib

from flask import Flask, request
from google.cloud import secretmanager_v1beta1
from hashlib import sha1


app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    signature = request.headers.get("X-Hub-Signature", None)
    body = request.data

    # Only process data with a valid signature
    assert verify_signature(signature, body), "Unverified Signature"

    publish_to_pubsub(body)

    sys.stdout.flush()
    return ("", 204)


def verify_signature(signature, body):
    expected_signature = "sha1="
    try:
        # Get secret from Cloud Secret Manager
        secret = get_secret(
            os.environ.get("PROJECT_NAME"), os.environ.get("SECRET_NAME"), "1"
        )
        # Compute the hashed signature
        hashed = hmac.new(secret, body, sha1)
        expected_signature += hashed.hexdigest()

    except Exception as e:
        print(e)

    return hmac.compare_digest(signature, expected_signature)


def publish_to_pubsub(msg):
    """
    Publishes the message to Cloud Pub/Sub
    """
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(
            os.environ.get("PROJECT_NAME"), os.environ.get("TOPIC_NAME")
        )

        # Pub/Sub data must be bytestring, attributes must be strings
        future = publisher.publish(topic_path, data=msg)

        exception = future.exception()
        if exception:
            raise Exception(exception)

        print(f"Published message: {future.result()}")

    except Exception as e:
        # Log any exceptions to stackdriver
        entry = dict(severity="WARNING", message=e)
        print(entry)


def get_secret(project_name, secret_name, version_num):
    # Returns secret payload from Cloud Secret Manager
    client = secretmanager_v1beta1.SecretManagerServiceClient()
    name = client.secret_version_path(project_name, secret_name, version_num)
    secret = client.access_secret_version(name)
    return secret.payload.data


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
