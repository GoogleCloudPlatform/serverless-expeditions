/*
Copyright 2021 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

const express = require("express");
const mysql = require("mysql");
const app = express();

app.use(express.json());
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`Dog Breed API listening on port ${port}`);
});

app.get("/", async (req, res) => {
  res.json({ status: "Bark bark! Ready to roll!" });
});

app.get("/:breed", async (req, res) => {
  const query = "SELECT * FROM breeds WHERE name = ?";
  try {
    (await getConnectionPool()).query(query, [req.params.breed], (error, results) => {
      if (!results[0]) {
        res.status(404).json({error: `${req.params.breed} not found.`});
      }
      else {
        res.json(results[0]);
      }
    });
  }
  catch (ex) {
    res.status(500).json({error: ex.toString()});
  }
});

let pool;

async function getConnectionPool() {
  if (!pool) {
    pool = mysql.createPool({
      user: process.env.DB_USER,
      password: await accessSecret('db_password'),
      database: process.env.DB_NAME,
      socketPath: `/cloudsql/${process.env.INSTANCE_CONNECTION_NAME}`,
    });
  }
  return pool;
}

const {SecretManagerServiceClient} = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

async function accessSecret(name, version='latest') {
  try {
    if (!process.env.GOOGLE_PROJECT_ID) {
      throw 'Please set the GOOGLE_PROJECT_ID environment variable.';
    }
    const fullName = `projects/${process.env.GOOGLE_PROJECT_ID}/secrets/` +
                     `${name}/versions/${version}`;
    const [response] = await client.accessSecretVersion({name: fullName});
    const payload = response.payload.data.toString();
    return payload;
  }
  catch (ex) {
    console.log(ex.toString());
  }
}
