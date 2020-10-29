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

    # Load the event as JSON for easier handling
    event = request.get_json(force=True)

    # Insert row into bigquery
    insert_row_into_bigquery(event)

    # Post new issues to Slack
    if event["action"] == "opened":
        issue_title = event["issue"]["title"]
        issue_url = event["issue"]["html_url"]
        send_issue_notification_to_slack(issue_title, issue_url)

        # Post response to Github
        create_issue_comment(event["issue"]["url"])

    print("Yay")

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


def send_issue_notification_to_slack(issue_title, issue_url):
    # Sends a message to Slack Channel
    msg = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"New issue created: <{issue_url}|{issue_title}>",
                },
            }
        ]
    }
    req = urllib.request.Request(
        os.environ.get("SLACK_URL"),
        data=json.dumps(msg).encode("utf8"),
        headers={"Content-Type": "application/json"},
    )
    response = urllib.request.urlopen(req)


def insert_row_into_bigquery(event):
    from google.cloud import bigquery

    # Set up bigquery instance
    client = bigquery.Client()
    dataset_id = os.environ.get("DATASET")
    table_id = os.environ.get("TABLE")
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Insert row
    row_to_insert = [
        (
            event["issue"]["title"],
            event["action"],
            event["issue"]["html_url"],
            time.time(),
        )
    ]
    bq_errors = client.insert_rows(table, row_to_insert)

    # If errors, log to Stackdriver
    if bq_errors:
        entry = {
            "severity": "WARNING",
            "msg": "Row not inserted.",
            "errors": bq_errors,
            "row": row_to_insert,
        }
        print(json.dumps(entry))


def create_issue_comment(api_url):
    # Posts an auto response to Github Issue

    # Get tokens
    pem = get_secret(os.environ.get("PROJECT_NAME"), os.environ.get("PEM"), "1")
    app_token = get_jwt(pem)
    installation_token = get_installation_token(app_token)

    # Create Github issue comment via HTTP POST
    try:
        msg = {
            "body": "Thank you for filing an issue. \
                 Someone will respond within 24 hours."
        }
        req = urllib.request.Request(
            api_url + "/comments", data=json.dumps(msg).encode("utf8")
        )
        req.add_header("Authorization", f"Bearer {installation_token}")
        response = urllib.request.urlopen(req)

    except Exception as e:
        print(e)


def get_jwt(pem):
    # Encodes and returns JWT
    from jwt import JWT, jwk_from_pem

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": os.environ.get("APP_ID"),
    }

    jwt = JWT()

    return jwt.encode(payload, jwk_from_pem(pem), "RS256")


def get_installation_token(jwt):
    # Get App installation token to use Github API
    req = urllib.request.Request(os.environ.get("INSTALLATION"), method="POST")
    req.add_header("Authorization", f"Bearer {jwt}")
    req.add_header("Accept", "application/vnd.github.machine-man-preview+json")

    response = urllib.request.urlopen(req)
    token_json = json.loads(response.read())
    return token_json["token"]


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
