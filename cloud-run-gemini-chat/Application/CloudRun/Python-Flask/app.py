'''
This application implements the Google Gemini REST API
'''

import json
import os

# Flask imports
from flask import Flask, request, Response, send_from_directory, render_template
from flask_wtf.csrf import CSRFProtect

#-------------------------------------------------------------------------------
# This local module fetches the Gemini API Key stored in Google Secrets Manager
#-------------------------------------------------------------------------------

from gcp_secrets import init_secrets

#-------------------------------------------------------------------------------
# This module implements the Google Gemini REST API
#-------------------------------------------------------------------------------

from gcp_gemini import ask_gemini

#-------------------------------------------------------------------------------
# This module implements various Google Cloud Project functions
#-------------------------------------------------------------------------------

from gcp_utils import get_project_id, get_client_ip

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
# Create the Flask application
#-------------------------------------------------------------------------------

app = Flask(__name__)

#-------------------------------------------------------------------------------
# TODO: Update with a different value
#-------------------------------------------------------------------------------

app.config["SECRET_KEY"] = ""

#-------------------------------------------------------------------------------
# CSRF - Cross Site Request Forgery
#-------------------------------------------------------------------------------

# app.config['WTF_CSRF_ENABLED'] = False
csrf = CSRFProtect(app)

#-------------------------------------------------------------------------------
# Utils
#-------------------------------------------------------------------------------

def create_response(msg):
	''' Accepts a string (msg) and returns JSON that the web browser app.js expects '''
	resp = { "text": msg }
	return json.dumps(resp)

#-------------------------------------------------------------------------------
# Routes
#-------------------------------------------------------------------------------

@app.after_request
def after_request(response):
	'''
	Flask does not log the correct client IP address on Cloud Run.
	Flask logs the proxy (GFE) address when running on Cloud Run.
	This function parses the HTTP request headers to determine the correct address.
	'''

	# print(f"Host: {get_host()}")
	print(f"Client IP: {get_client_ip()}")
	return response

@app.route("/", methods = ["GET"])
def home():
	''' Return the website home page '''
	return render_template("index.html", client_ip=get_client_ip())

@app.route("/about", methods = ["GET"])
def about():
	''' Return the website about page '''
	return render_template("about.html", client_ip=get_client_ip())

@app.route("/gemini", methods = ["GET"])
def gemini():
	''' Return the website gemini page '''
	return render_template("gemini.html", client_ip=get_client_ip())

@app.route("/app.js", methods = ["GET"])
def app_js():
	''' Return the file app.js '''
	return send_from_directory("static", "app.js")

@app.route("/favicon.ico", methods = ["GET"])
def fav_ico():
	''' Return the file favicon.ico '''
	return send_from_directory("static", "favicon.ico", mimetype='image/vnd.microsoft.icon')

# @csrf.exempt
@app.route("/ask", methods = ["POST"])
def ask():
	''' Endpoint that accepts a JSON POST request '''
	data = request.get_json()

	model = data.get("model")
	question = data.get("text")

	answer = ask_gemini(gemini_api_key, model, question)

	return Response(create_response(answer), mimetype='application/json')

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

#-------------------------------------------------------------------------------
# This section only runs if started by Python
# Does not run under gunicorn
#-------------------------------------------------------------------------------

if __name__ == "__main__":
	debugFlag = os.environ.get("FLASK_DEBUG", False)

	if debugFlag == "False":
		debugFlag = False
		print('Debug disable')
	elif debugFlag == "True":
		debugFlag = True
		print('Debug enabled')

	app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
