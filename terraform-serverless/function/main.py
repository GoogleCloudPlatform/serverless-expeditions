import io

from flask import jsonify
from google.cloud import storage, vision
from PIL import Image

vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()


def detect_cat(request):
    """
    param:
      bucket: gcs bucket
      resource: gcs bucket resource

    returns:
      information about the image

    Testing data: {"bucket": "glasnt-terraform-3476-test", "resource": "loan-7AIDE8PrvA0-unsplash.jpg"}

    """
    bucket = request.args.get("bucket", None)
    resource = request.args.get("resource", None)

    if not bucket:
        return "Invalid invocation: require bucket", 400

    if not resource:
        return "Invalid invocation: require resource", 400

    uri = f"gs://{bucket}/{resource}"

    data = {}

    blob = storage_client.bucket(bucket).get_blob(resource).download_as_bytes()

    # Image specifics
    img = Image.open(io.BytesIO(blob))
    data["image_details"] = {
        "height": img.height,
        "width": img.width,
        "format": img.format,
    }

    # Vision API Labels
    vision_image = vision.Image()
    vision_image.source.image_uri = uri
    response = vision_client.label_detection(image=vision_image)
    labels = response.label_annotations
    data["labels"] = [label.description for label in labels]

    # Cat?
    data["is_cat"] = "Cat" in data["labels"]

    return jsonify(data)
