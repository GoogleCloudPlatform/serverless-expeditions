# Cloud Run Always-on CPU Allocation Weather Advisory app

This is the corresponding code repo for the [Serverless Expeditions](https://goo.gle/ServerlessExpeditions) video covering the [Cloud Run Always-on CPU Allocation feature](https://cloud.google.com/run/docs/configuring/cpu-allocation) that [launched in Fall 2021](https://cloud.google.com/blog/products/serverless/cloud-run-gets-always-on-cpu-allocation). It is currently available in Node.js.

## Application files

File | Description
--- | ---
[`main.js`](index.js) | main application file
[`templates/index.html`](templates/index.html) | application HTML template
[`package.json`](package.json) | 3rd-party package requirements file
[`.gcloudignore`](.gcloudignore) | files to exclude deploying to the cloud (administrative)
`README.md` | this file (administrative)

Below are the required settings and instructions to deploy this application.


## **Local Express server (Node 10, 17)**

**TL;DR:** application files (`index.js` &amp; `package.json`) plus `credentials.json`. Instructions:

1. **Run** `npm install` (to install packages locally)
1. **Run** `gcloud auth application-default login` to set your credentials
1. **Run** `npm start` to run locally


## **Cloud Run (Node 10+ via Cloud Buildpacks)**

**TL;DR:** Uses only the application files. Instruction(s):

1. **Run** `gcloud run deploy weater --allow-unauthenticated --platform managed` to deploy to Cloud Run; optionally add `--source . --region REGION` for non-interactive deploy
    - A `Dockerfile` is optional, but if you wish to create one, place it in the top-level folder so the build system can access it.


## The application itself

The app consists of a simple web page prompting the user for a US state (or territory) abbreviation to fetch the latest weather advisories from the US NOAA Weather API. The results along with the selected state are presented along with an empty form for a follow-up request if desired. Results are cached for 15 minutes.

This is what the app UI looks like upon an initial `GET` of its home page:

![GET app screenshot](https://user-images.githubusercontent.com/1102504/153354509-3afdad1a-d5ca-4463-91fe-ee95d3e0b150.png)


This is what the app looks like after completing one weather request (for Maryland):

![POST app screenshot](https://user-images.githubusercontent.com/1102504/153354523-51a58bb6-66b3-4251-95cd-63217ee86edc.png)


## References

- [Serverless Expeditions](https://goo.gle/ServerlessExpeditions) video series
- [Cloud Run Always-on CPU Allocation](https://cloud.google.com/run/docs/configuring/cpu-allocation)
- [Always-on CPU launch announcement](https://cloud.google.com/blog/products/serverless/cloud-run-gets-always-on-cpu-allocation)
- [Node.js Cloud Run quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/nodejs)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Cloud Run home page](http://cloud.run)
- [Express.js](https://expressjs.com)

