'''
This module implements utilities for the Google Gemini REST API
	https://ai.google.dev/tutorials/rest_quickstart
'''

def get_gemini_model_endpoint(model):
	''' Determine which Gemini model to use and return the REST URL '''

	host = "https://generativelanguage.googleapis.com"

	#---------------------------------------------------------------------
	# Validate model
	#---------------------------------------------------------------------

	if model is None or len(model) == 0:
		# Default to model (Gemini 1.0 Pro)
		model = "gemini_1_0_pro_latest"

	#---------------------------------------------------------------------
	# Select the Gemini LLM model to use
	#---------------------------------------------------------------------

	if model == "gemini_1_0_pro_latest":
		path = "/v1beta/models/gemini-1.0-pro-latest:generateContent"
	elif model == "gemini_1_0_ultra_latest":
		path = "/v1beta/models/gemini-1.0-ultra-latest:generateContent"
	elif model == "gemini_1_5_pro_latest":
		path = "/v1beta/models/gemini-1.5-pro-latest:generateContent"
	else:
		# Default model (Gemini 1.0 Pro)
		path = "/v1beta/models/gemini-pro:generateContent"

	return host + path

def get_gemini_response_text(resp):
	''' Process the Gemini response and return the content text '''

	text = ''

	candidates = resp["candidates"]

	for candidate in candidates:
		parts = candidate["content"]["parts"]

		for part in parts:
			text += part.get("text", "")

	return text
