# /usr/env/python3
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from pydoc import doc
import re

from google.cloud import documentai_v1 as documentai
from google.cloud import firestore
from google.cloud import storage

INCOMING_PREFIX = "incoming/"

db = firestore.Client()


# Use Document AI to examine a PDF invoice, provided as a Cloud Storage Blob,
# and return information in a Document AI object.
def process_blob(
    project_id: str, location: str, processor_id: str, blob: storage.blob.Blob
):
    """
    Applies the specified DocumentAI processor to the contents of the Blob
    """

    # Instantiate a synchronous Document AI client
    client_options = {
        "api_endpoint": "{}-documentai.googleapis.com".format(location)}
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    resource_name = client.processor_path(project_id, location, processor_id)

    # Read the file into memory
    doc = {"content": blob.download_as_bytes(), "mime_type": blob.content_type}

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=doc)

    # Recognizes text entities in the PDF document
    result = client.process_document(request=request)

    return result.document


def document_info(document):
    """
        Creates a Python dict with needed data from the processed document object.
    """
    info = {"lines": []}
    
    for entity in document.entities:
        if entity.type_ == "line_item":
            line = {}
            for property in entity.properties:
                line[property.type_] = property.mention_text
            info["lines"].append(line)
        else:
            info[entity.type_] = entity.mention_text
    
    return info


# Pull the desired data from the Document AI document and save in Firestore DB
def save_processed_document(document, blob):
    collection = os.getenv("COLLECTION", "invoices")

    info = document_info(document)

    total_string = re.sub(r"[,\$]", "", info.get("total_amount", "N/A"))
    try:
        total = float(total_string)
    except:
        total = 0.0

    paid_string = re.sub(r"[,\$]", "", info.get("amount_paid_since_last_invoice", "N/A"))
    try:
        paid = float(paid_string)
    except:
        paid = 0.0

    rounded_total = "{:.2f}".format(total)
    rounded_amount_due = "{:.2f}".format(total - paid)

    data = {
        "blob_name": blob.name[len(INCOMING_PREFIX):],
        "company": info.get("supplier_name", "Missing name"),
        "date": info.get("invoice_date", "N/A").strip(),
        "due_date": info.get("due_date", "N/A").strip(),
        "total": rounded_total,
        "amount_due": rounded_amount_due,
        "state": "Not Approved"
    }

    db.collection(collection).document(data["blob_name"]).set(data)