# Cloud Run Always-on CPU Allocation Weather Advisory app

This is the corresponding code repo for the [Serverless Expeditions](https://goo.gle/ServerlessExpeditions) [video](http://youtu.be/ul1cGarS23M) covering the [Cloud Run Always-on CPU Allocation feature](https://cloud.google.com/run/docs/configuring/cpu-allocation) that [launched in Fall 2021](https://cloud.google.com/blog/products/serverless/cloud-run-gets-always-on-cpu-allocation).

More information on this sample can be found in the video's [announcement blog post](https://cloud.google.com/blog/topics/developers-practitioners/use-cloud-run-always-cpu-allocation-background-work) (social post [here](https://twitter.com/GoogleCloudTech/status/1511450354189316099)).


## The code

This app is available in [Python](python) and [Node.js](nodejs).

Language | Versions | Deployment | Framework
--- | --- | --- | ---
Python|2.7|local|Flask
Python|3.6+|local, Cloud Run|Flask
Node.js|10, 17|local|Express.js
Node.js|10, 12, 14, 16|Cloud Run|Express.js


## Application components

The app consist of 7 primary functions, each of which plays a pivotal role, and they direct fetching of the data from the API, caching it, or retrieving it from the cache for the end-user. Those functions are listed here:

Function name | Description
--- | ---
`stateIsInCache()` | Are weather alerts for one state cached and "fresh?"
`fetchState()` | Fetch weather alerts for one state from API
`cacheState()` | Cache weather alerts for one state
`getStateFromCache()` | Get alerts for one state from cache
`app.all()` (JS) or `root()` (Py) | Main app: handle all `GET` and `POST` requests
`updateCache()` | Check each state and refresh cache as necessary
`setInterval()` (JS) or `_setInterval()` (Py) | Thread running every 5 minutes to update cache

The interval thread calling `updateCache()` are the pieces leveraging Cloud Run's "always-on" CPU allocation because they run _after_ the request has responded. Typically the CPU is throttled at this time, the 15 minutes before an instance is shut down due to lack of traffic. Always-on CPU allocation provides 100% CPU so background tasks like refreshing the cache can take place during this time.

Other functions are either for support or administrative purposes. Specific information on each app is available in each app's `README`.


## The application itself

### Operation

The app consists of a simple web page prompting the user for a US state (or territory) abbreviation to fetch the latest weather advisories from the US NOAA Weather API. The results along with the selected state are presented along with an empty form for a follow-up request if desired. Results are cached for 15 minutes.

This is what the app UI looks like upon an initial `GET` of its home page:

![GET app screenshot](https://user-images.githubusercontent.com/1102504/153354509-3afdad1a-d5ca-4463-91fe-ee95d3e0b150.png)
This is what the app looks like after completing one weather request (for Maryland):

![POST app screenshot](https://user-images.githubusercontent.com/1102504/153354523-51a58bb6-66b3-4251-95cd-63217ee86edc.png)

### Code

The most interesting piece of code is probably `stateIsInCache()`. It has to check whether a state's weather advisories is currently cached as well as whether that cached entry is "fresh," meaning newer than 15 minutes.

![stateIsInCache](https://user-images.githubusercontent.com/1102504/164938783-a28f31fc-8ea5-473d-bd69-1e6e4850e8d9.png)

On the other hand, the most boring bit of code is the most critical, `updateCache()`. It leverages the "always-on CPU" allocation feature and is set to update the cache every 5 minutes until the container instance is shut down via `setInterval()`:

![updateCache](https://user-images.githubusercontent.com/1102504/164938716-f30db4cf-fcde-46e6-b6cd-5f668a80943b.png)


## Costs

### Billing required and free tier

Google Cloud Run is not a free service; all applications require an [active billing account](https://cloud.google.com/billing). However, Cloud Run (and other GCP products) do have an ["Always Free" tier](https://cloud.google.com/free/docs/gcp-free-tier#free-tier-usage-limits) and as long as you stay within those limits, you shouldn't incur any charges. Also check the Cloud Run [pricing](https://cloud.google.com/run/pricing) and [quotas &amp; limits](https://cloud.google.com/run/quotas) pages for more information.

### Build &amp; storage costs

Deploying to [GCP serverless platforms](https://cloud.google.com/serverless) incur [minor build and storage costs](https://cloud.google.com/appengine/pricing#pricing-for-related-google-cloud-products). [Cloud Build](https://cloud.google.com/build/pricing) has its own free quota as does [Cloud Storage](https://cloud.google.com/storage/pricing#cloud-storage-always-free). For greater transparency, Cloud Build builds your application image which is than sent to the [Cloud Container Registry](https://cloud.google.com/container-registry/pricing), or [Artifact Registry](https://cloud.google.com/artifact-registry/pricing), its successor. Storage of that image uses up some of that (Cloud Storage) quota as does network egress when transferring that image to the service you're deploying to. However you may live in region that does not have such a free tier, so be aware of this type of usage to minimize potential costs. (You may observe your storage usage, and delete prior build artifacts if desired, via the [Cloud Storage browser](https://console.cloud.google.com/storage/browser) for your GCP project.)

### Cleanup

As this is a sample app, you don't want to incur ongoing billing, so release its resources once you've completed your analysis of this app and its CPU allocation feature. You can [disable](https://cloud.google.com/run/docs/managing/services#disable) or [delete](https://cloud.google.com/run/docs/managing/services#delete) the Cloud Run service, or [shutdown your GCP project entirely](https://console.cloud.google.com/iam-admin/settings).


## References

- [Serverless Expeditions](https://goo.gle/ServerlessExpeditions) video series
- [Cloud Run Always-on CPU Allocation](https://cloud.google.com/run/docs/configuring/cpu-allocation)
- [Always-on CPU launch announcement](https://cloud.google.com/blog/products/serverless/cloud-run-gets-always-on-cpu-allocation)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Cloud Run home page](http://cloud.run)
