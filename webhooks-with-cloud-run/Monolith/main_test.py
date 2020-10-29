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
import json

from hashlib import sha1

import main

import mock
import pytest


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_empty_payload(client):
    with pytest.raises(Exception) as e:
        client.post("/")


@mock.patch("main.get_secret", mock.MagicMock(return_value=b"foo"))
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


@mock.patch("main.get_secret", mock.MagicMock(return_value=b"foo"))
def test_insert_into_bq_called(client):
    data = json.dumps({"action": "foobar"}).encode("utf-8")

    signature = "sha1=" + hmac.new(b"foo", data, sha1).hexdigest()

    main.insert_row_into_bigquery = mock.MagicMock(return_value=True)
    main.send_issue_notification_to_slack = mock.MagicMock(return_value=True)
    main.create_issue_comment = mock.MagicMock(return_value=True)

    r = client.post("/", data=data, headers={"X-Hub-Signature": signature},)

    main.insert_row_into_bigquery.assert_called_with(json.loads(data))
    assert r.status_code == 204


@mock.patch("main.get_secret", mock.MagicMock(return_value=b"foo"))
@mock.patch("main.insert_row_into_bigquery", mock.MagicMock())
@mock.patch("main.create_issue_comment", mock.MagicMock())
def test_slack_api_called(client):

    data = json.dumps(
        {
            "action": "opened",
            "issue": {"title": "foo", "html_url": "bar", "url": "foobar"},
        }
    ).encode("utf-8")

    signature = "sha1=" + hmac.new(b"foo", data, sha1).hexdigest()
    main.send_issue_notification_to_slack = mock.MagicMock(return_value=True)

    r = client.post("/", data=data, headers={"X-Hub-Signature": signature},)

    main.send_issue_notification_to_slack.assert_called_with("foo", "bar")
    assert r.status_code == 204


@mock.patch("main.get_secret", mock.MagicMock(return_value=b"foo"))
@mock.patch("main.insert_row_into_bigquery", mock.MagicMock())
@mock.patch("main.send_issue_notification_to_slack", mock.MagicMock())
def test_issue_comment_called(client):

    data = json.dumps(
        {
            "action": "opened",
            "issue": {"title": "foo", "html_url": "bar", "url": "foobar"},
        }
    ).encode("utf-8")

    signature = "sha1=" + hmac.new(b"foo", data, sha1).hexdigest()
    main.create_issue_comment = mock.MagicMock(return_value=True)

    r = client.post("/", data=data, headers={"X-Hub-Signature": signature},)

    main.create_issue_comment.assert_called_with("foobar")
    assert r.status_code == 204
