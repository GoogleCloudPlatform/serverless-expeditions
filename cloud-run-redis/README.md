## README

This simple Cloud Run service demonstrates how to implement a read-through and
write-through cache in front of a database. To keep things simple, the database
is implemented in an in-memory array and it always takes 3 seconds to read from
it or write to it. The cache is using Memorystore for Redis.


### deploy.sh

Use this to deploy the code to your own GCP project. Before you run this script,
do these things:
  * Create a Memorystore instance in your GCP project.
  * Create a Serverless VPC Connector instance in your GCP project.
  * Set values for the environment variables on lines 1-5 of deploy.sh.


### Artist REST API.postman_collection.json

Once you have deployed your Cloud Run service, you can test it with Postman.
To do that:
  * Open the file *Artist REST API.postman_collection.json* in a text editor,
  replace "rest-api-3ap6wvqypa-uc" with the corresponding URL part of the
  Cloud Run service you deployed to your project.
  * Then import the file into Postman by clicking the Import button near the top
  left corner.
  * You can now click and invoke the methods to view artists, update an artist,
  view the contents of the cache, and flush the cache.

