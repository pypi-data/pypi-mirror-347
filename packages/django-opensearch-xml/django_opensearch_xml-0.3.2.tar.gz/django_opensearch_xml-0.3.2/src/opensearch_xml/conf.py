"""
conf for :mod:`opensearch_xml` application.

:creationdate:  12/06/2024 09:31
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: opensearch_xml.conf
"""
import logging

from appconf import AppConf

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class OpenSearchXMLAppConf(AppConf):
    """App configuration for :mod:`opensearch_xml`."""

    CONTACT_EMAIL: str = ""
    SHORT_NAME: str = ""
    DESCRIPTION: str = ""
    FAVICON_WIDTH: int = 16
    FAVICON_HEIGHT: int = 16
    FAVICON_TYPE: str = "image/x-icon"
    FAVICON_FILE: str = "favicon.ico"
    SEARCH_URL: str = "search"
    SEARCH_QUERYSTRING: str = "q="
    INPUT_ENCODING: str = "UTF-8"

    class Meta:
        """Metaclass for `opensearch_xml.conf.OpenSearchXMLAppConf`."""

        prefix = "opensearch_xml"
