# Cloud Run sample for Cloud Spanner

## Dependencies
- [Locust](https://locust.io)
- [Docker](https://www.docker.com) or Cloud Run
- A Cloud Spanner instance or [Cloud Spanner Emulator](https://cloud.google.com/spanner/docs/emulator)


## Authentication
If running with Cloud Run and a Spanner instance, this app uses a service account with the the ability to read and write to the Spanner database. For simplicity, the pre-defined role `roles/spanner.databaseReader` will work.

## Setup
- Create Spanner schema from the `schema.sql` file.
- Build the app docker image and run it.
- Run the `locustfile.py` and open webbrowser to `localhost`

