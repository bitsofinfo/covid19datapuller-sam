import json

import pytest

from covid19datapuller import app


@pytest.fixture()
def dummy_event():
    """ Generates API GW Event"""

    return {
        "whatever": 'value',
    }


def fetch(dummy_event, mocker):

    ret = app.fetch(dummy_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "version" in ret["body"]
