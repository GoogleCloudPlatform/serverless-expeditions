import os
import tempfile

import flask
import requests
from google.cloud import storage

BUCKET_NAME = os.environ.get("BUCKET_NAME")
FUNCTION_NAME = os.environ.get("FUNCTION_NAME")

app = flask.Flask(__name__)
storage = storage.Client()
bucket = storage.bucket(BUCKET_NAME)


@app.route("/cat/<img>")
def cat(img):
    blob = bucket.blob(img)
    with tempfile.NamedTemporaryFile() as temp:
        blob.download_to_filename(temp.name)
        return flask.send_file(temp.name, attachment_filename=img)


def get_cats(bucket):
    images = storage.list_blobs(BUCKET_NAME)

    # auth when running a privte function
    # https://cloud.google.com/functions/docs/securing/authenticating#functions-bearer-token-example-python
    if "cloudfunctions.net" in FUNCTION_NAME:
        metadata_server_url = "http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience="
        token_full_url = metadata_server_url + FUNCTION_NAME
        token_headers = {"Metadata-Flavor": "Google"}

        token_response = requests.get(token_full_url, headers=token_headers)
        jwt = token_response.text
        function_headers = {"Authorization": f"bearer {jwt}"}
    else:
        function_headers = {}

    cats = []
    for img in images:
        resp = requests.get(
            FUNCTION_NAME,
            params={"bucket": BUCKET_NAME, "resource": img.name},
            headers=function_headers,
        )
        cats.append({"image": img, "data": resp.json()})

    return cats


@app.route("/")
def hello_cats():
    if not BUCKET_NAME:
        return flask.render_template_string(
            "Missing environment variable: BUCKET_NAME."
        )

    if not FUNCTION_NAME:
        return flask.render_template_string(
            "Missing environment variable: FUNCTION_NAME."
        )

    cats = get_cats(BUCKET_NAME)
    have_cat = any([c["data"]["is_cat"] for c in cats])
    return flask.render_template("cats.html", cats=cats, have_cat=have_cat)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
