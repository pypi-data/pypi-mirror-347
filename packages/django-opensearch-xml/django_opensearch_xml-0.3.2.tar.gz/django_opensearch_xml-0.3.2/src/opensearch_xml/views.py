"""
views for :mod:`opensearch_xml` application.

:creationdate:  13/06/2024 08:26
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: opensearch_xml.views
"""

import logging
from typing import Any

from django.conf import settings
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import resolve_url
from django.template.loader import render_to_string

__author__ = "fguerin"
logger = logging.getLogger(__name__)


def opensearch_xml(request: HttpRequest) -> HttpResponse:
    """Render OpenSearch XML page."""
    if settings.STATIC_URL.startswith("http") or settings.STATIC_URL.startswith("//"):
        _favicon_file = settings.STATIC_URL + settings.OPENSEARCH_XML_FAVICON_FILE
    else:
        _favicon_file = request.build_absolute_uri(settings.STATIC_URL + settings.OPENSEARCH_XML_FAVICON_FILE)
    context: dict[str, Any] = {
        "CONTACT_EMAIL": settings.OPENSEARCH_XML_CONTACT_EMAIL,
        "SHORT_NAME": settings.OPENSEARCH_XML_SHORT_NAME,
        "DESCRIPTION": settings.OPENSEARCH_XML_DESCRIPTION,
        "FAVICON_WIDTH": settings.OPENSEARCH_XML_FAVICON_WIDTH,
        "FAVICON_HEIGHT": settings.OPENSEARCH_XML_FAVICON_HEIGHT,
        "FAVICON_TYPE": settings.OPENSEARCH_XML_FAVICON_TYPE,
        "FAVICON_FILE": _favicon_file,
        "URL": "{url}?{querystring}{{searchTerms}}".format(  # noqa: FS002
            **{
                "url": request.build_absolute_uri(resolve_url(to=settings.OPENSEARCH_XML_SEARCH_URL)),
                "querystring": settings.OPENSEARCH_XML_SEARCH_QUERYSTRING,
            }
        ),
        "INPUT_ENCODING": settings.OPENSEARCH_XML_INPUT_ENCODING.upper(),
    }
    output = render_to_string("opensearch_xml/opensearch.xml", context)
    logger.debug("opensearch_xml()\n%s", output)
    if settings.DEBUG:
        from xml.dom.minidom import parseString  # noqa: S408

        temp = parseString(output)  # noqa: S318
        logger.debug("opensearch_xml()\n%s", temp.toprettyxml())
    return HttpResponse(
        output,
        content_type="application/opensearchdescription+xml",
        status=200,
    )
