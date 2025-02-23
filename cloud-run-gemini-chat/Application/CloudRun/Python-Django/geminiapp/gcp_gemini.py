'''
This module implements the Google Gemini REST API
	https://ai.google.dev/tutorials/rest_quickstart
'''

import json
import requests

#-------------------------------------------------------------------------------
# Markdown to HTML converter
#-------------------------------------------------------------------------------

import markdown

#-------------------------------------------------------------------------------
# This module implements utilities for the Google Gemini REST API
#-------------------------------------------------------------------------------

from .gcp_gemini_utils import get_gemini_model_endpoint, get_gemini_response_text

def ask_gemini(api_key, model, question):
	''' Interact with Google Gemini '''

	#---------------------------------------------------------------------
	# Google Gemini REST API Documentation
	# https://ai.google.dev/api/rest
	#---------------------------------------------------------------------

	#---------------------------------------------------------------------
	# Validate api_key
	#---------------------------------------------------------------------

	if api_key is None or len(api_key) == 0:
		return "Internal Error: Missing API Key"

	#---------------------------------------------------------------------
	# Verify question parameter
	#
	# TODO: Validate question
	#	Only the string length for zero is checked at this time.
	#	What is the maximum length supported. Gemini specifies token
	#	which is about 4 characters.
	#	https://ai.google.dev/models/gemini
	#	Gemini 1.0 Pro input token limit is 30,720.
	#	Gemini 1.5 Pro input token limit is 1,048,576.
	#---------------------------------------------------------------------

	if question is None or len(question) == 0:
		return "Please enter a question"

	#---------------------------------------------------------------------
	# Get the Gemini Model to use
	#---------------------------------------------------------------------

	url = get_gemini_model_endpoint(model)

	headers = {
		"x-goog-api-key": api_key,
		"Content-type": "application/json"
	}

	#---------------------------------------------------------------------
	# Format the JSON request
	#---------------------------------------------------------------------

	data = {
		"contents": [
			{
				"parts":[
					{
						"text": question
					}
				]
			}
		]
	}

	#---------------------------------------------------------------------
	# Issue the HTTP POST request
	#---------------------------------------------------------------------

	try:
		# print(json.dumps(data, indent=4))	# debug

		response = requests.post(url, headers=headers, json=data, timeout=120)

		# print(response.status_code)		# debug
		# print(response.content)		# debug

		if response.status_code == 404:
			print(response.content)		# print error message
			msg = "**Error: The Gemini model is not available for your project or does not exist**"
			return markdown.markdown(msg)

		if response.status_code >= 400:
			print(response.content)		# print error message
			msg = "**Error: Request to Gemini failed**"
			return markdown.markdown(msg)

		#---------------------------------------------------------------------
		# Process the output
		# TODO: This needs better handling.
		#       Gemini returns various formats that are not yet documented.
		#	An important item is to process the key "finishReason".
		#	Normal requests return "STOP", but I have seen "SAFETY"
		#	which means the request was rejected. See the link:
		#	https://ai.google.dev/api/rest/v1/GenerateContentResponse#FinishReason
		#
		# https://ai.google.dev/api/rest/v1/Content
		#---------------------------------------------------------------------

		resp = response.json()

		# print(json.dumps(resp, indent=4))	# debug

		reason = resp["candidates"][0]["finishReason"]

		# print("Reason:", reason)	# debug

		if reason == "STOP":
			# Good status
			text = get_gemini_response_text(resp)
		elif reason == "MAX_TOKENS":
			# Error
			text = "**Gemini Error: The maximum number of tokens as specified in the request was reached.**"
		elif reason == "RECITATION":
			# Error
			text = "**Gemini Error: The candidate content was flagged for recitation reasons.**"
		elif reason == "SAFETY":
			# Error
			text = "**Gemini Error: The candidate content was flagged for safety reasons.**"
		else:
			# Error
			text = f"**Gemini Error: Gemini refused the question for {reason}**"

		#---------------------------------------------------------------------
		# Gemini returns Markdown, convert to HTML
		#---------------------------------------------------------------------

		html = markdown.markdown(text, extensions=['tables'])
		return html.replace('<table>', '<table class="table table-striped">')
	except Exception as e:
		print(e)		# print error message
		return None
