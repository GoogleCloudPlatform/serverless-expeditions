# Cloud Run Always-on CPU Allocation Weather Advisory app

This is the corresponding code repo for the [Serverless Expeditions](https://goo.gle/ServerlessExpeditions) video covering the [Cloud Run Always-on CPU Allocation feature](https://cloud.google.com/run/docs/configuring/cpu-allocation) that [launched in Fall 2021](https://cloud.google.com/blog/products/serverless/cloud-run-gets-always-on-cpu-allocation).


## The code

It is available in [Python](python) and [Node.js](nodejs).

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

The app consists of a simple web page prompting the user for a US state (or territory) abbreviation to fetch the latest weather advisories from the US NOAA Weather API. The results along with the selected state are presented along with an empty form for a follow-up request if desired. Results are cached for 15 minutes.

This is what the app UI looks like upon an initial `GET` of its home page:

![GET app screenshot](https://user-images.githubusercontent.com/1102504/153354509-3afdad1a-d5ca-4463-91fe-ee95d3e0b150.png)
This is what the app looks like after completing one weather request (for Maryland):

![POST app screenshot](https://user-images.githubusercontent.com/1102504/153354523-51a58bb6-66b3-4251-95cd-63217ee86edc.png)


## References

- [Serverless Expeditions](https://goo.gle/ServerlessExpeditions) video series
- [Cloud Run Always-on CPU Allocation](https://cloud.google.com/run/docs/configuring/cpu-allocation)
- [Always-on CPU launch announcement](https://cloud.google.com/blog/products/serverless/cloud-run-gets-always-on-cpu-allocation)
- [Cloud Run documentation](https://cloud.google.com/run/docs)
- [Cloud Run home page](http://cloud.run)
