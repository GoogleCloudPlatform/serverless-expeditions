'''
This application implements the Google Gemini REST API
'''

import os
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.template import loader

#-------------------------------------------------------------------------------
# This local module fetches the Gemini API Key stored in Google Secrets Manager
#-------------------------------------------------------------------------------

from .gcp_secrets import init_secrets

#-------------------------------------------------------------------------------
# This module implements the Google Gemini REST API
#-------------------------------------------------------------------------------

from .gcp_gemini import ask_gemini

#-------------------------------------------------------------------------------
# This module implements various Google Cloud Project functions
#-------------------------------------------------------------------------------

from .gcp_utils import get_project_id	# , get_client_ip, get_host

#-------------------------------------------------------------------------------
# Set the Project ID for Secrets Manager when running locally.
# In Cloud Run the Project ID will be read from the Metadata service
#-------------------------------------------------------------------------------

gcp_project_id = os.environ.get("GCP_PROJECT_ID", None)

#-------------------------------------------------------------------------------
# Google Cloud Secret Manager secret name
#-------------------------------------------------------------------------------

SECRET_NAME = "GEMINI_API_KEY"

#-------------------------------------------------------------------------------
# The Gemini API Key read from Google Secrets Manager
#-------------------------------------------------------------------------------

gemini_api_key = None

#-------------------------------------------------------------------------------
# Utils
#-------------------------------------------------------------------------------

def create_response(msg):
	''' Accepts a string (msg) and returns JSON that the web browser app.js expects '''
	resp = { "text": msg }
	return resp

@ensure_csrf_cookie
def index(request, *args, **kwargs):
	''' This view serves the home (index) page '''
	''' TODO: FIX code to handle Client IP in template '''
	template = loader.get_template('index.html')
	return HttpResponse(template.render())

def app_js(request, *args, **kwargs):
	''' This view serves the app.js file '''
	with open("geminiapp/static/app.js", 'rb') as f:
		data = f.read()

	return HttpResponse(data, headers={'Content-Type': 'text/javascript'})

def favicon(request, *args, **kwargs):
	''' This view serves the favicon.ico image '''
	with open("geminiapp/static/favicon.ico", 'rb') as f:
		data = f.read()

	return HttpResponse(data, headers={'Content-Type': 'image/vnd.microsoft.icon'})

def about(request, *args, **kwargs):
	''' This view serves the about page '''
	''' TODO: FIX code to handle Client IP in template '''
	template = loader.get_template('about.html')
	return HttpResponse(template.render())

def gemini(request, *args, **kwargs):
	''' This view serves the gemini page '''
	''' TODO: FIX code to handle Client IP in template '''
	template = loader.get_template('gemini.html')
	return HttpResponse(template.render())

# @csrf_exempt		# use when testing to turn off CSRF
@csrf_protect
def ask(request, *args, **kwargs):
	''' Endpoint that accepts a JSON POST request '''
	data = json.loads(request.body)

	model = data["model"]
	question = data["text"]

	answer = ask_gemini(gemini_api_key, model, question)

	return JsonResponse(create_response(answer))

#-------------------------------------------------------------------------------
# BEGIN - Initialize app
#-------------------------------------------------------------------------------

if gcp_project_id is None:
	project_id = get_project_id()
	if project_id is not None:
		gcp_project_id = project_id
if gcp_project_id is None:
	print("Error: Cannot set the Project ID")

if gemini_api_key is None:
	gemini_api_key = init_secrets(gcp_project_id, SECRET_NAME)
if gemini_api_key is None:
	print("Error: Cannot fetch Gemini API Key")

# print(f"Project ID: Key {gcp_project_id}")	# debug
# print(f"Gemini API Key: {gemini_api_key}")	# debug
