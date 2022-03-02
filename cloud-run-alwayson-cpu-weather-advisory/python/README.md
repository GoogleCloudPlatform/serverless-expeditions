# Cloud Run Always-on CPU Allocation Weather Advisory app (Python)

This is the Python version of the sample app. It is Python 2 (2.7) and 3 (3.6+) compatible. You can run this app locally using the Flask development server in either Python 2 or 3. The Cloud Run deployment as-is only supports Python 3. If you wish to run this on Cloud Run with Python 2, an appropriate `Dockerfile` is required (more below). The app is also available in [Node.js](../nodejs).


## Application files

File | Description
--- | ---
[`main.py`](main.py) | main application file
[`templates/index.html`](templates/index.html) | application HTML template
[`requirements.txt`](requirements.txt) | 3rd-party package requirements file
[`.gcloudignore`](.gcloudignore) | files to exclude deploying to the cloud (administrative)
`README.md` | this file (administrative)

You can run this locally or on Cloud Run. Below are the required settings and instructions to do each.


## **Local Flask server (Python 2 or 3)**

1. **Run** `pip install -r requirements.txt` ([or `pip2` or `pip3`] to install packages locally)
1. **Run** `gcloud auth application-default login` to set your credentials
1. **Run** `python main.py` to run locally (or `python2` or `python3`)


## **Cloud Run (Python 3.6+ via Cloud Buildpacks)**

1. **Run** `gcloud run deploy weather --allow-unauthenticated --platform managed` to deploy to Cloud Run; optionally add `--source . --region REGION` for non-interactive deploy
    - A `Dockerfile` is optional, but if you wish to create one, place it in the top-level folder so the build system can access it.
    - Deploying this as a Python 2 to Cloud Run requires a [supporting `Dockerfile`](https://github.com/googlecodelabs/cloud-nebulous-serverless/blob/main/cloud/python/Dockerfile).



## References

- [Google Cloud support for Python](https://cloud.google.com/python)
- [Flask](https://flask.palletsprojects.com)

