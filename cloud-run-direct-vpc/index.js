// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

const express = require('express');
const app = express();
app.use(express.json());
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`API listening on port ${port}`);
});

const redisClient = require('redis').createClient(
  process.env.REDIS_PORT,
  process.env.REDIS_HOST
);

// Read one artist, by id.
app.get('/artist/:id', async (req, res) => {
  try {
    const id = req.params.id;
    const artist = await getArtistFromCache(id);
    if (artist) {
      res.json(artist);
      return;
    }
    else {
      res.status(404).json({error: `Artist ${id} not found`});
    }
  }
  catch(ex) {
    res.status(500).json({error: ex.toString()});
  }
})

async function getArtistFromDatabase(id) {
  const sleep = require('util').promisify(setTimeout);
  await sleep(3000); // Simulate a slow database query.
  return artistsInDatabase.find(artist => artist.id==id);
}

async function getArtistFromCache(id) {
  const { promisify } = require("util");
  const redisGet = promisify(redisClient.get).bind(redisClient);
  const redisExists = promisify(redisClient.exists).bind(redisClient);
  if (! await redisExists(id)) {
    const artist = await getArtistFromDatabase(id);
    if (artist) {
      redisClient.set(id, JSON.stringify(artist));
    }
  }
  return JSON.parse(await redisGet(id));
}

// Return all artists currently in the database.
app.get('/database', async (req, res) => {
  res.json(artistsInDatabase);
})

// Return all artists currently in the cache.
app.get('/cache', async (req, res) => {
  const { promisify } = require("util");
  const redisKeys = promisify(redisClient.keys).bind(redisClient);
  const redisGet = promisify(redisClient.get).bind(redisClient);
  const ids = await redisKeys('*');
  const artistsInCache = [];
  for (id of ids) {
    const artist = JSON.parse(await redisGet(id));;
    artistsInCache.push(artist);
  }
  res.json(artistsInCache);
})

// Delete all artists from the Redis cache.
app.post('/flush-cache', async (req, res) => {
  redisClient.flushdb((err, succeeded) => {
    res.json({status: "Cache flushed"});
  });
})

// This array is the fake database. Using a fake database to make it easier to
// experiment with caching strategies without having to set up and maintain a
// real database.
const artistsInDatabase = [
  {
    id: '1',
    name: 'Frida Kahlo',
    born: 'July 6, 1907, Coyoacán, Mexico City, Mexico',
    died: 'July 13, 1954, Coyoacán, Mexico City, Mexico',
    notableWorks: [
      'The Two Fridas (1939)',
      'Self-Portrait with Thorn Necklace and Hummingbird (1940)',
      'The Broken Column (1944)'
    ],
  },
  {
    id: '2',
    name: 'Diego Rivera',
    born: 'December 8, 1886, Guanajuato City, Mexico',
    died: 'November 24, 1957, Mexico City, Mexico',
    notableWorks: [
      'Detroit Industry Murals (1933)',
      'Man, Controller of the Universe (1934)',
      'The History of Mexico (1935)'
    ],
  },
]
