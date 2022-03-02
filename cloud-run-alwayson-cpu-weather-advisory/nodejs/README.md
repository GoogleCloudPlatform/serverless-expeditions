# Cloud Run Always-on CPU Allocation Weather Advisory app (Node.js)

This is the Node.js/JavaScript version of the sample app. It has been tested locally with Node 10 and 17, and deploys to Cloud Run with the current supported version (Node 14 at the time of this writing). The app is also available in [Python](../python).


## Application files

File | Description
--- | ---
[`main.js`](main.js) | main application file
[`templates/index.html`](templates/index.html) | application HTML template
[`package.json`](package.json) | 3rd-party package requirements file
[`.gcloudignore`](.gcloudignore) | files to exclude deploying to the cloud (administrative)
`README.md` | this file (administrative)

You can run this locally or on Cloud Run. Below are the required settings and instructions to do each.


## **Local Express server (Node 10, 17)**

1. **Run** `npm install` (to install packages locally)
1. **Run** `gcloud auth application-default login` to set your credentials
1. **Run** `npm start` to run locally


## **Cloud Run (Node 14 via Cloud Buildpacks)**

1. **Run** `gcloud run deploy weather --allow-unauthenticated --platform managed` to deploy to Cloud Run; optionally add `--source . --region REGION` for non-interactive deploy
    - A `Dockerfile` is optional, but if you wish to create one, place it in the top-level folder so the build system can access it.


## References

- [Node.js Cloud Run quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/nodejs)
- [Google Cloud support for Node.js](https://cloud.google.com/nodejs)
- [Express.js](https://expressjs.com)

