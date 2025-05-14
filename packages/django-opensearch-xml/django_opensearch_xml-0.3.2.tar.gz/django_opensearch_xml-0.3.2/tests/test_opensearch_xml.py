"""Tests for :mod:`opensearch_xml` package."""

# ruff: noqa: S101
from typing import Any
from xml.dom import minidom  # noqa: S408

import pytest
from django.template.loader import render_to_string

OPENSEARCH_PARAMS: list[dict[str, Any]] = [
    {
        "CONTACT_EMAIL": "fguerin@ville-tourcoing.fr",
        "SHORT_NAME": "Documentation",
        "DESCRIPTION": "Documentation",
        "FAVICON_WIDTH": 16,
        "FAVICON_HEIGHT": 16,
        "FAVICON_FILE": "images/favicon.png",
    }
]


@pytest.fixture(scope="module", params=OPENSEARCH_PARAMS)
def opensearch_xml_params(request) -> dict[str, Any]:
    """Get the OpenSearch XML parameters."""
    return request.param


def test_opensearch_xml(opensearch_xml_params: dict[str, Any]):
    """Test the opensearch xml rendering."""
    xml = render_to_string("opensearch.xml", opensearch_xml_params)
    assert xml

    dom = minidom.parseString(xml)  # noqa: S318
    assert dom.getElementsByTagName("Contact")[0].firstChild.nodeValue == opensearch_xml_params["CONTACT_EMAIL"]
    assert dom.getElementsByTagName("ShortName")[0].firstChild.nodeValue == opensearch_xml_params["SHORT_NAME"]
    assert dom.getElementsByTagName("Description")[0].firstChild.nodeValue == opensearch_xml_params["DESCRIPTION"]
    assert dom.getElementsByTagName("InputEncoding")[0].firstChild.nodeValue == "UTF-8"
    assert dom.getElementsByTagName("Image")[0].attributes["width"] == opensearch_xml_params["FAVICON_WIDTH"]
    assert dom.getElementsByTagName("Image")[0].attributes["height"] == opensearch_xml_params["FAVICON_HEIGHT"]
    assert opensearch_xml_params["FAVICON_FILE"] in dom.getElementsByTagName("Image")[0].firstChild.nodeValue
