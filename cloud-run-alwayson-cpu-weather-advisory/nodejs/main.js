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

const port = process.env.PORT || 8080;
const url = 'https://api.weather.gov/alerts/active?area=';
const STATES = [
    'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
    'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
    'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
    'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY',
];

app.listen(port, () => {
    console.log(`** Listening on port ${port}`);
});


async function getStateFromCache(state) {
    const query = DATASTORE.createQuery('State').filter('state', '=', state);
    const [results] = await DATASTORE.runQuery(query);
    return results.length ? results[0] : null;
}


async function stateIsInCache(state) {  // check data in-cache & fresh
    const fma = new Date(new Date() - 15*60*1000);  // "15 minutes ago"
    const stateData = await getStateFromCache(state);
    const useCache = stateData ? (stateData.lastUpdate > fma) : false;
    console.log(useCache ? `** Cache fresh, use in-cache data (${state})` :
        `** Cache stale/missing, API fetch (${state})`)
    return useCache;
}


async function fetchState(state) {  // fetch state info from API
    const api_rsp = await axios.get(url + state); // issue weather API request
    const advisories = api_rsp.data.features;
    const savedAdvisories = advisories.map(advisory => {
        const prop = advisory.properties;
        return {  // process each advisory
            area: prop.areaDesc,
            state: state,
            headline: ('NWSheadline' in prop.parameters) ?
                prop.parameters.NWSheadline[0] :
                prop.headline,
            effective: prop.effective,
            expires: prop.expires,
            instructions: (!prop.instruction) ? '(none)' :
                prop.instruction.replace(/\n/g, ' '),
        }
    });
    return savedAdvisories;
}


async function cacheState(state, advisories) {  // cache state info
    const entity = {
        key: DATASTORE.key(['State', state]),
        data: {
            state: state,
            advisories: advisories,
            lastUpdate: new Date(),  // last-fetched timestamp
        }
    };
    await DATASTORE.save(entity);
}


app.all('/', async (req, rsp) => {
    let context = {meth: req.method, state: 'CA'};
    if (req.method === 'POST') {
        let state;
        try {
            state = req.body.state.trim().slice(0, 2).toUpperCase() || 'CA';
            context.state = state;
            if (!(await stateIsInCache(state))) {
                const advisories = await fetchState(state);
                await cacheState(state, advisories);
            }
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


async function updateCache() {
    // check each state and update cache as necessary
    for (let state of STATES) {
        if (!(await stateIsInCache(state))) {
            const advisories = await fetchState(state);
            await cacheState(state, advisories);
        }
    }
}


// always-on CPU refreshes cache every 5 minutes (max 3x per always-on CPU)
setInterval(() => {
    updateCache();
}, 300 * 1000);


module.exports = {
    app
};
