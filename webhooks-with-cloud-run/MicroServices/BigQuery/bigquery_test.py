# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json

import bigquery

import mock
import pytest


@pytest.fixture
def client():
    bigquery.app.testing = True
    return bigquery.app.test_client()


def test_not_json(client):
    with pytest.raises(Exception) as e:
        client.post("/", data="foo")

    assert "Expecting JSON payload" in str(e.value)


def test_not_pubsub_message(client):
    with pytest.raises(Exception) as e:
        client.post(
            "/",
            data=json.dumps({"foo": "bar"}),
            headers={"Content-Type": "application/json"},
        )

    assert "Not a valid Pub/Sub Message" in str(e.value)


def test_insert_into_bq_called(client):
    data = json.dumps({"foo": "bar"}).encode("utf-8")
    pubsub_msg = {
        "message": {"data": base64.b64encode(data).decode("utf-8")},
    }

    bigquery.insert_row_into_bigquery = mock.MagicMock(return_value=True)

    r = client.post(
        "/",
        data=json.dumps(pubsub_msg),
        headers={"Content-Type": "application/json"},
    )

    bigquery.insert_row_into_bigquery.assert_called_with({"foo": "bar"})
    assert r.status_code == 204
