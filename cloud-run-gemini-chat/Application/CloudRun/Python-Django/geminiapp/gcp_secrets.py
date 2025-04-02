'''
This module fetches the Gemini API Key stored in Google Secrets Manager
	https://cloud.google.com/python/docs/reference/secretmanager/latest
'''

# Google Secrets Manager imports
from google.cloud import secretmanager_v1

def init_secrets(project_id, secret_name):
	''' Fetch the GEMINI_API_KEY stored in Google Secrets Manager '''

	try:
		#---------------------------------------------------------------------
		# Secrets Manager reports an error if byte strings are used
		#---------------------------------------------------------------------

		if isinstance(project_id, bytes):
			project_id = project_id.decode('utf-8')

		if isinstance(secret_name, bytes):
			secret_name = secret_name.decode('utf-8')

		#---------------------------------------------------------------------
		# Initialize the Secrets Manager Client
		#---------------------------------------------------------------------

		client = secretmanager_v1.SecretManagerServiceClient()

		#---------------------------------------------------------------------
		# Format the secret name
		# In app.py, the secret name is set by SECRET_NAME
		#---------------------------------------------------------------------

		name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"

		#---------------------------------------------------------------------
		# Build the client request
		#---------------------------------------------------------------------

		req = secretmanager_v1.AccessSecretVersionRequest(
			name=name
		)

		#---------------------------------------------------------------------
		# Fetch the secret
		#---------------------------------------------------------------------

		response = client.access_secret_version(request=req)

		api_key = response.payload.data.decode('utf-8')

		return api_key
	except Exception as e:
		print(e)		# print error message
		return None
