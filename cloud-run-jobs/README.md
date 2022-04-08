# Cloud Run Jobs Nightly Invoice Processing

This is the corresponding code repo for the
[Serverless Expeditions](https://www.youtube.com/playlist?list=PLIivdWyY5sqJwq_pgOxcHzusWjXDVCEiX)
video covering the Cloud Run Jobs feature
that will launch in early 2022.

This job uses [Document AI](https://cloud.google.com/document-ai)
the process data from human-readable invoices
in a variety of file formats stored in a
[Cloud Storage](https://cloud.google.com/storage) bucket,
and saves that data in a
[Cloud Firestore](https://cloud.google.com/firestore) database.

## The code

The program being executed is in `main.py`. That program
calls code from the `process.py` module to work with
The Document AI and Cloud Firestore client libraries.

A variation of the program that can be used to break
the work down into up to 16 parallel tasks is in
`main-tasks.py`. Rename that to `main.py` when
creating the container to be able to run multiple
tasks at once.

The Dockerfile defines a basic container to run Python
programs.

## Prepare for the job

Create a Google Cloud project using the console or command
line, and enable the Cloud Run API and Cloud Document API.

Use the console to navigate the the
[Document AI](https://console.cloud.google.com/ai/document-ai)
section and create a new _Invoice Parser_ processor.

You will also need to create a bucket in the command line
or the console to hold invoices to process. New invoices
should be place in a bucket folder called `incoming/` and
the file names should start with a lower-case hex digit
(one of 0123456789abcdef). Naming them with UUID4 value
works well.

Note the Bucket name, Cloud Project ID, and the Document AI Processor ID
which will be used in the command to create the job.


## Create the Cloud Run Job

Cloud Run Jobs can create a job from a container. The
container can be built with a variety of tools, including
Google Cloud Build with the command:

    gcloud builds submit --tag=gcr.io/my-cloud-project-id/name-for-job

Once a container is available in a container repository, create
the job with the command:

    gcloud run jobs create [NAME OF NEW JOB] \
    --image=gcr.io/[MY CLOUD PROJECT ID]/[NAME OF NEW JOB]
    --region=[REGION, e.g. us-central1] \
    --tasks=[NUMBER OF PARALLEL TASKS]
    --set-env-vars=BUCKET=[NAME OF BUCKET WITH INVOICES] \
    --set-env-vars=PROCESSOR_ID=[INVOICE PROCESSOR ID]

If you used the original `main.py` file when building the container
for the job, use 1 for the _NUMBER OF PARALLEL TASKS_,
since that job doesn't include logic to divide the work
into separate tasks. If you used the `main_tasks.py` file
instead, set tasks to the number of tasks you want to
use. Note that that program's logic is such that only
up to 16 tasks will actually do any processing. Tasks
beyond the 16th will run, determine that there is no work
for them, and exit.

## Run the job

Run the job from the command line with the command:

    gcloud run jobs execute [NAME OF NEW JOB]

or in the console by navigating the the _Cloud Run_ section
selecting the _Jobs_ tab and clicking the name of
the job.
