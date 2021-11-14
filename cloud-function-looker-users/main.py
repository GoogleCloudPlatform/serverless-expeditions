from googleapiclient.discovery import build
import google.auth
import looker_sdk
sdk = looker_sdk.init40()

def main(request):
  """Take email from a column inside an existing Google Sheet"""
  try: 
    all_emails = get_email_from_sheet() # returns [['email1'], ['email2'], ['email3']]
    for item in all_emails:
      email = item[0]
      create_users(email=email)
    return f'Successfully created {len(all_emails)} new Looker users.'
  except:
    return 'An error occurred.'

def get_email_from_sheet():
  """Authenticate to an existing Google Sheet using the default runtime 
  service account and read all email addresses from a column inside the sheet.
  Refer to README.md for details about using Default App Engine Service Account 
  for authentication. 
  """
  # Get the key of an existing Google Sheet from the URL. 
  # Example: https://docs.google.com/spreadsheets/d/[KEY HERE]/edit#gid=111
  SAMPLE_SPREADSHEET_ID = "foo"

  # Google Sheet Range: https://developers.google.com/sheets/api/samples/reading
  SAMPLE_RANGE_NAME = "Sheet1!B:B" # all cells in column B, Sheet1

  creds, _proj_id = google.auth.default()
  service = build("sheets", "v4", credentials=creds)
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()  
  all_emails = result.get('values', []) 
  return all_emails 

def create_users(email):
  """Use Looker Python SDK to make new users"""
  new_user = sdk.create_user(
            body=looker_sdk.models40.WriteUser(
                credentials_email=looker_sdk.models40.WriteCredentialsEmail(
                    email=email,
                    forced_password_reset_at_next_login=False
                ),
                is_disabled=False,
                models_dir_validated=False
            )
        )
  # Create email credentials for the new user
  sdk.create_user_credentials_email(
                user_id=new_user.id,
                body=looker_sdk.models40.WriteCredentialsEmail(
                    email=email,
                    forced_password_reset_at_next_login=False
                ))
  # Send a welcome/setup email
  sdk.send_user_credentials_email_password_reset(user_id=new_user["id"])
    