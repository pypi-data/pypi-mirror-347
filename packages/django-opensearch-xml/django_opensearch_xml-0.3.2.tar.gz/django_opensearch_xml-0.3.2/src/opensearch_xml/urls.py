"""
urls for :mod:`opensearch_xml` application.

:creationdate:  13/06/2024 08:40
:moduleauthor: François GUÉRIN <fguerin@ville-tourcoing.fr>
:modulename: opensearch_xml.urls
"""

import logging

from django.urls import path

from opensearch_xml import views

__author__ = "fguerin"
logger = logging.getLogger(__name__)

app_name = "opensearch_xml"
urlpatterns = [
    path("", views.opensearch_xml, name="xml"),
]
