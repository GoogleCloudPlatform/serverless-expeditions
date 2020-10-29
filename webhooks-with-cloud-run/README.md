# Webhooks on Cloud Run

This repository contains the code for the Serverless Expeditions episodes
Webhooks with Cloud Run [part 1](https://youtu.be/53MCPoFr03E),
[part 2](https://youtu.be/tsKZ_u_uIAs).

The code demonstrates how to use Cloud Run to host a webhook target. It
processes events from Github to:

1. Send notifications to Slack.
1. Stream to BigQuery.
1. Send a response back to Github.

The *Monolith* directory contains the first draft of the webhook, where all the
processing is done in one process. The *Microservices* directory contains the
more robust version of the app, that is less sensitive to timeouts and
temporary outages.

