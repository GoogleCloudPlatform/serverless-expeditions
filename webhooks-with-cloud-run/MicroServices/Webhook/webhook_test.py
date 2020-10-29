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

import hmac
from hashlib import sha1

import webhook

import mock
import pytest


@pytest.fixture
def client():
    webhook.app.testing = True
    return webhook.app.test_client()


def test_empty_payload(client):
    with pytest.raises(Exception) as e:
        client.post("/")


@mock.patch("webhook.get_secret", mock.MagicMock(return_value=b"foo"))
def test_unverified_signature(client):
    with pytest.raises(Exception) as e:
        client.post(
            "/",
            headers={
                "User-Agent": "GitHub-Hookshot",
                "X-Hub-Signature": "foobar",
            },
        )

    assert "Unverified Signature" in str(e.value)


@mock.patch("webhook.get_secret", mock.MagicMock(return_value=b"foo"))
@mock.patch("webhook.publish_to_pubsub", mock.MagicMock(return_value=True))
def test_verified_signature(client):
    signature = "sha1=" + hmac.new(b"foo", b"Hello", sha1).hexdigest()
    r = client.post("/", data="Hello", headers={"X-Hub-Signature": signature},)
    assert r.status_code == 204


@mock.patch("webhook.get_secret", mock.MagicMock(return_value=b"foo"))
def test_data_sent_to_pubsub(client):
    signature = "sha1=" + hmac.new(b"foo", b"Hello", sha1).hexdigest()
    webhook.publish_to_pubsub = mock.MagicMock(return_value=True)
    headers = {
        "X-Hub-Signature": signature,
    }

    r = client.post("/", data="Hello", headers={"X-Hub-Signature": signature},)

    webhook.publish_to_pubsub.assert_called_with(b"Hello")
    assert r.status_code == 204
