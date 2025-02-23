'''
This module implements various Google Cloud Project functions
'''
# Flask imports
from flask import request

import requests

def get_project_id():
	'''
	This function reads the Google Cloud Project ID from the Metadata service
	'''

	try:
		url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
		# url = "http://metadata.goog/v1/project/project-id"

		headers = {
			"Metadata-Flavor": "Google"
		}

		response = requests.get(url, headers=headers, timeout=0.5)

		if response.status_code >= 400:
			print(response.content)		# print error message
			return None

		return response.content.decode("utf-8")
	except Exception as e:
		print(e)		# print error message
		return None

def get_client_ip():
	'''
	Returns the client IP address.
	That IP might be IPv4 or IPv6 depending on how the client connected.
	'''

	if "x-forwarded-for" in request.headers:
		return request.headers.getlist("x-forwarded-for")[0].rpartition(" ")[-1]

	return request.remote_addr

def get_host():
	'''
	Returns the host header
	
	On Google Cloud Run the HTTP Host header cannot be forged.
	1) The host header is used by the GFE to know which Cloud Run instance to forware to.
	2) The GFE only forwards HTTPS requets. That means the host header must match
	   one of the managed certificates.
	'''
	if "host" in request.headers:
		return request.headers.get("host", "localhost")

	return "localhost"
