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

from hashlib import sha1
from flask import Flask, request

from google.cloud import secretmanager_v1beta1
from google.cloud import bigquery


app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()

    # Check if valid JSON
    if not envelope:
        raise Exception("Expecting JSON payload")
    # Check if valid pub/sub message
    if "message" not in envelope:
        raise Exception("Not a valid Pub/Sub Message")

    msg = envelope["message"]
    data = json.loads(base64.b64decode(msg["data"]).decode("utf-8").strip())

    # Insert row into bigquery
    insert_row_into_bigquery(data)

    print("Yay")

    sys.stdout.flush()
    return ("", 204)


def insert_row_into_bigquery(data):
    # Set up bigquery instance
    client = bigquery.Client()
    dataset_id = os.environ.get("DATASET")
    table_id = os.environ.get("TABLE")
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Insert row
    row_to_insert = [
        (
            data["issue"]["title"],
            data["action"],
            data["issue"]["html_url"],
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


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
