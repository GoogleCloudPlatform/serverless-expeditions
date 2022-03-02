// Copyright 2022 Google LLC
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

const axios = require('axios');
const express = require('express');
const nunjucks = require('nunjucks');
const {Datastore} = require('@google-cloud/datastore');

const app = express();
app.use(express.urlencoded({extended: true}));
nunjucks.configure('templates', {autoescape: true, express: app});
const DATASTORE = new Datastore();
const DEFAULT = 'CA';
const MINUTE = 60 * 1000;
const PORT = process.env.PORT || 8080;
const URL = 'https://api.weather.gov/alerts/active?area=';
const STATES = [
    'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
    'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
    'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
    'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY',
];

app.listen(PORT, () => {
    console.log(`** Listening on port ${PORT}`);
});


// get state alerts from cache
async function getStateFromCache(state) {
    const query = DATASTORE.createQuery('State')
        .filter('__key__', '=', DATASTORE.key(['State', state]));
    const [results] = await DATASTORE.runQuery(query);
    return results.length ? results[0] : null;
}


// check if state alerts are in cache & "fresh"
async function stateIsInCache(state) {
    const fma = new Date(new Date() - 15*MINUTE);  // "15 minutes ago"
    const stateData = await getStateFromCache(state);
    const useCache = stateData ? (stateData.lastUpdate > fma) : false;
    console.log(useCache ? `** Cache fresh, use in-cache data (${state})` :
        `** Cache stale/missing, API fetch (${state})`)
    return useCache;
}


// fetch state weather alerts from API
async function fetchState(state) {
    const api_rsp = await axios.get(URL + state);  // call weather API
    const advisories = api_rsp.data.features;
    return advisories.map(advisory => {
        const prop = advisory.properties;
        return {  // extract/format relevant weather alert data
            area:         prop.areaDesc,
            headline:     ('NWSheadline' in prop.parameters) ?
                prop.parameters.NWSheadline[0] : prop.headline,
            effective:    prop.effective,
            expires:      prop.expires,
            instructions: (!prop.instruction) ? '(none)' :
                prop.instruction.replace(/\n/g, ' '),
        }
    });
}


// cache state weather alerts to Datastore
async function cacheState(state, advisories) {
    const entity = {
        key: DATASTORE.key(['State', state]),
        data: {
            advisories: advisories,
            lastUpdate: new Date(),  // last-fetched timestamp
        }
    };
    await DATASTORE.save(entity);
}


// check if state in cache & fresh; fetch & cache if not
async function processState(state) {
    if (!(await stateIsInCache(state))) {
        const advisories = await fetchState(state);
        await cacheState(state, advisories);
    }
}


// main application handler (GET/POST)
app.all('/', async (req, rsp) => {
    let context = {meth: req.method, state: DEFAULT};
    // GET: render empty form
    // POST: process user request, display results, render empty form
    if (req.method === 'POST') {
        let state;
        try {
            state = req.body.state.trim().slice(0, 2).toUpperCase() || DEFAULT;
            context.state = state;
            await processState(state);
            const stateData = await getStateFromCache(state);
            if (stateData) {
                context.advs = stateData.advisories;
            } else {
                context.error = `ERROR: problem with request for ${state}`;
            }
        }
        catch (ex) {
            const error = `ERROR: problem with request for ${state}: ${ex.toString()}`;
            console.error(error);
            context.error = error;
        }
    }
    rsp.render('index.html', context);
})


// check each state and update cache as necessary
async function updateCache() {
    for (let state of STATES) {
        await processState(state);
    }
}


// always-on CPU refreshes cache every 5 minutes
// (max 3x per always-on CPU re 15 min shutdown)
setInterval(() => {
    updateCache();
}, 5*MINUTE);


module.exports = {
    app
};
