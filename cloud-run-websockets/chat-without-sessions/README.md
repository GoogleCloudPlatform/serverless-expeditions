# Node.js websockets sample for Cloud Run

This sample demonstrates how to use websockets on
[Cloud Run][run] with Node.js.

* [Setup](#setup)
* [Running locally](#running-locally)
* [Deploying to App Engine](#deploying-to-app-engine)
* [Running the tests](#running-the-tests)

## Setup

Before you can run or deploy the sample, you need to do the following:

1.  Refer to the [run/README.md][readme] file for instructions on
    running and deploying.
1.  Install dependencies:

    With `npm`:

        npm install

## Running locally

With `npm`:

    npm start

## Deploying to Cloud Run

    gcloud beta run deploy websocket --source . --allow-unauthenticated

## Running the tests

See [Contributing][contributing].

[run]: https://cloud.google.com/run/docs
[readme]: ../README.md
[contributing]: https://github.com/GoogleCloudPlatform/nodejs-docs-samples/blob/master/CONTRIBUTING.md