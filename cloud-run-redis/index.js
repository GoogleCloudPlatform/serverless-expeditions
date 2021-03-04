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

// Update an artist. The payload should contain an id field, plus any fields
// that should be updated or added to the artist record.
app.put('/artist', async (req, res) => {
  try {
    const artistUpdate = req.body;
    await updateArtistInCache(artistUpdate);
    res.json({status: "Success"});
  }
  catch(ex) {
    res.status(500).json({error: ex.toString()});
  }
})

async function updateArtistInCache(artistUpdate) {
  // If two requests update the same artist at the same time, the code below
  // *might* put stale data into the cache. If your application is updating JSON
  // objects very frequently, consider using https://oss.redislabs.com/redisjson
  const artist = await getArtistFromCache(artistUpdate.id);
  if (artist) {
    Object.assign(artist, artistUpdate);
    redisClient.set(artist.id, JSON.stringify(artist));
    await updateArtistInDatabase(artistUpdate);
  }
}

async function updateArtistInDatabase(artistUpdate) {
  const sleep = require('util').promisify(setTimeout);
  await sleep(3000); // Simulate a slow database write.
  const artist = artistsInDatabase.find(a => a.id==artistUpdate.id);
  if (artist) {
    Object.assign(artist, artistUpdate);
  }
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
