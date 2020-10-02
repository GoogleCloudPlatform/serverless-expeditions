# Using Python on Google Cloud with Cloud Run

This sample is a simple Cloud Run service written in Python.
It converts Euros to USD.

Build and deploy this service by running the following commands:

```
$ gcloud builds submit --tag gcr.io/PROJECT_ID/euro-to-usd

$ gcloud run deploy --image gcr.io/PROJECT_ID/euro-to-usd
--platform managed
```

If you don't want to deploy a new Cloud Run service, install the Cloud Code plugin ([VS Code](https://marketplace.visualstudio.com/items?itemName=GoogleCloudTools.cloudcode&ssr=false#overview) | [JetBrains](https://plugins.jetbrains.com/plugin/8079-cloud-code)) and run it in a Cloud Run emulator ([VS Code](https://cloud.google.com/code/docs/vscode/developing-a-cloud-run-app) | [JetBrains](https://cloud.google.com/code/docs/intellij/developing-a-cloud-run-app)).


For more info, check out this sample's accompanying [Serverless Expeditions video](https://www.youtube.com/watch?v=s2TIWIzCftM).