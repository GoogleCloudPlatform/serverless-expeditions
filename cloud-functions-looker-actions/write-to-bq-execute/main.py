from google.cloud import bigquery
import json, os, requests

def main(request):
    auth = authenticate(request)
    if auth: 
        table_title = write_data_to_csv(request)
        load_table_file(file_path="/tmp/table.csv",table_title=table_title)
    return {
        'statusCode': 200,
        'body': json.dumps('action_execute received')
    }

def authenticate(request):
  submitted_secret = request.headers['Authorization'] #Token token="secret"
  secret = os.environ.get("LOOKER_ACTION_BIGQUERY_SECRET")
  expected_secret = 'Token token="{}"'.format(secret)   
  if expected_secret == submitted_secret:
    return True

def write_data_to_csv(request):
  payload = request.get_json()
  download_url = payload["scheduled_plan"]["download_url"]
  table_title = payload["scheduled_plan"]["title"]
  r = requests.get(download_url, allow_redirects=True)
  open('/tmp/table.csv', 'wb').write(r.content)
  return table_title

def load_table_file(file_path,table_title):
    client = bigquery.Client()
    table_id = "myproject.mydataset." + table_title # Replace "myproject.mydataset." with your project
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )
    with open(file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_id, job_config=job_config)
    job.result()  # Wait for the job to complete.
    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )
    return "200"
