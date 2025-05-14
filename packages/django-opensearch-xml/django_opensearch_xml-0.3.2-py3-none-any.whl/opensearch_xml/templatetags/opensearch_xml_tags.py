"""
opensearch_xml_tags_tags for the :mod:`opensearch_xml` application.

:creationdate: 12/06/2024
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: opensearch_xml.templatetags.opensearch_xml_tags_tags
"""

import logging
from typing import Any

from django import template
from django.conf import settings

logger = logging.getLogger(__name__)
register = template.Library()


@register.inclusion_tag("opensearch_xml/tags/opensearch_xml_meta.html")
def opensearch_xml_meta() -> dict[str, Any]:
    """Return OpenSearch metadata."""
    return {
        "debug": settings.DEBUG,
        "DESCRIPTION": settings.OPENSEARCH_XML_DESCRIPTION,
    }


@register.inclusion_tag("opensearch_xml/tags/opensearch_xml_meta.html")
def opensearch_meta() -> dict[str, Any]:
    """
    Return OpenSearch metadata.

    .. note:: Alias for ``opensearch_xml_meta``.
    """
    return opensearch_xml_meta()
