## README

This simple Cloud Run service demonstrates how to implement a read-through and
write-through cache in front of a database. To keep things simple, the database
is implemented in an in-memory array and it always takes 3 seconds to read from
it or write to it. The cache is using Memorystore for Redis.


### deploy.sh

Use this to deploy the code to your own GCP project. Before you run this script,
do these things:
  * Create a Memorystore instance in your GCP project.
  * Set values for the environment variables on lines 1-4 of deploy.sh.
