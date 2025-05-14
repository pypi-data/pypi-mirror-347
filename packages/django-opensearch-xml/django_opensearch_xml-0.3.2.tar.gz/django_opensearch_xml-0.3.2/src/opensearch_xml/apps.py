"""
apps for :mod:`opensearch_xml` application.

:creationdate:  13/06/2024 08:20
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: opensearch_xml.apps
"""
import logging

from django.apps import AppConfig

__author__ = "fguerin"
logger = logging.getLogger(__name__)


class OpenSearchXmlAppConfig(AppConfig):
    """:mod:`opensearch_xml` app configuration."""

    name = "opensearch_xml"

    def ready(self) -> None:
        """Perform some operations when application is ready."""
        super().ready()
        logger.debug("%s::ready()", self.__class__.__name__)
        from opensearch_xml import conf  # noqa
