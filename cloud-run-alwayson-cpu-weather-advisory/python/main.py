# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import atexit
from datetime import datetime as dt
import os
from time import mktime, time
from threading import Event, Thread

from flask import Flask, render_template, request
import requests
from google.cloud import datastore

app = Flask(__name__)
DATASTORE = datastore.Client()
DEFAULT = 'CA'
MINUTE = 60
URL = 'https://api.weather.gov/alerts/active?area=%s'
STATES = frozenset((
    'AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
    'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
    'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH',
    'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT', 'WA', 'WI', 'WV', 'WY',
))


def getStateFromCache(state):
    'get state alerts from cache'
    query = DATASTORE.query(kind='State')
    query.key_filter(DATASTORE.key('State', state))
    results = list(query.fetch())
    return results[0] if len(results) else None


def stateIsInCache(state):
    'check if state alerts are in cache & "fresh"'
    useCache = False
    fma = time() - 15*MINUTE  # "15 minutes ago"
    stateData = getStateFromCache(state)
    if stateData:
        ts = stateData['lastUpdate']
        lastUpdate = ts.timestamp() if hasattr(ts, 'timestamp') \
                else mktime(ts.timetuple())
        useCache = lastUpdate > fma
    print(('** Cache fresh, use in-cache data (%s)' if useCache \
            else '** Cache stale/missing, API fetch (%s)') % state)
    return useCache


def _etl(advisory, state):
    'extract/format relevant weather alert data'
    prop = advisory['properties']
    return {
        'area':         prop['areaDesc'],
        'headline':     prop['parameters']['NWSheadline'][0] \
                if 'NWSheadline' in prop['parameters'] else prop['headline'],
        'effective':    prop['effective'],
        'expires':      prop['expires'],
        'instrutions':  prop['instruction'].replace('\n', ' ') \
                if prop['instruction'] else '(none)'
    }


def fetchState(state):
    'fetch state weather alerts from API'
    rsp = requests.get(URL % state)  # call weather API
    if rsp.status_code >= 400:
        rsp.raise_for_status()
    advisories = rsp.json()['features']
    return [_etl(advisory, state) for advisory in advisories]


def cacheState(state, advisories):  # cache state info
    'cache state weather alerts to Datastore'
    entity = datastore.Entity(key=DATASTORE.key('State', state))
    entity.update({
        'advisories': advisories,
        'lastUpdate': dt.utcnow(),  # last-fetched timestamp
    })
    DATASTORE.put(entity)


def processState(state):
    'check if state in cache & fresh; fetch & cache if not'
    if not stateIsInCache(state):
        advisories = fetchState(state)
        cacheState(state, advisories)


@app.route('/', methods=['GET', 'POST'])
def root():
    'main application handler (GET/POST)'
    context = {'meth': request.method, 'state': DEFAULT}
    # GET: render empty form
    # POST: process user request, display results, render empty form
    if request.method == 'POST':
        try:
            state = request.form['state'].strip()[:2].upper() or DEFAULT
            context['state'] = state
            processState(state)
            stateData = getStateFromCache(state)
            if stateData:
                context['advs'] = stateData['advisories']
            else:
                context['error'] = 'ERROR: problem with request for {%s}' % state
        except Exception as e:
            error = 'ERROR: problem with request for %s: %s' % (state, e)
            print(error)
            context['error'] = error
    return render_template('index.html', **context)


def _setInterval(func, interval):
    'mimic JS setInterval() - call return value to stop'
    stop = Event()
    def loop():
        while not stop.wait(interval):
            func()
    Thread(target=loop).start()
    return stop.set


def updateCache():
    'check each state and update cache as necessary'
    for state in STATES:
        processState(state)


if __name__ == '__main__':
    # always-on CPU refreshes cache every 5 minutes
    # (max 3x per always-on CPU re 15 min shutdown)
    atexit.register(_setInterval(updateCache, 5*MINUTE))
    app.run('0.0.0.0', int(os.environ.get('PORT', 8080)))
