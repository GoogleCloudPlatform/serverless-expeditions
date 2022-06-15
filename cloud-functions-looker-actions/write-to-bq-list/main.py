from icon import icon_data_uri
import os

def authenticate(request):
  submitted_secret = request.headers['Authorization'] #Token token="secret"
  secret = os.environ.get("LOOKER_ACTION_BIGQUERY_SECRET")
  expected_secret = 'Token token="{}"'.format(secret)   
  if expected_secret == submitted_secret:
    return True

def main(request):
  auth = authenticate(request)
  if auth: 
    actions_list = {
      "integrations": [
        {
          "name": "send_to_bq",
          "label": "Send to BQ",
          "description": "Send the result of this query to BigQuery",
          "supported_action_types": ["query"],
          "supported_formats": ["csv"],
          "url": "url-to-the-execute-function",
          "icon_data_uri": icon_data_uri,
          "supported_download_settings": ["url"]
        }
      ]
    }
    return actions_list

