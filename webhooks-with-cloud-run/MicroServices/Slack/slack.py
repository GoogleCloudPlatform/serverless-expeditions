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
    # Subscribes to Pub/Sub Topic
    # and sends a message to Slack Channel
    envelope = request.get_json()

    # Assert data has been posted
    assert envelope, "Expecting JSON payload"
    # Assert is a valid pub/sub message
    assert "message" in envelope, "Not a valid Pub/Sub Message"

    msg = envelope["message"]
    data = json.loads(base64.b64decode(msg["data"]).decode("utf-8").strip())

    if data["action"] == "opened":
        issue_title = data["issue"]["title"]
        issue_url = data["issue"]["html_url"]
        send_issue_notification_to_slack(issue_title, issue_url)

    sys.stdout.flush()
    return ("", 204)


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


if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host="127.0.0.1", port=PORT, debug=True)
