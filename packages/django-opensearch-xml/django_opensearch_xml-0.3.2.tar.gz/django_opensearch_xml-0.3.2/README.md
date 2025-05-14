# OpenSearch application for django

This application provide a way to integrate the [OpenSearch](https://developer.mozilla.org/en-US/docs/Web/OpenSearch)
XML file to a django application.

[[_TOC_]]

## Installation

Install the package `pip install django-opensearch-xml`

## Configuration

+ Add "opensearch_xml" to settings.INSTALLED_APPS.
  ```python
  INSTALLED_APPS = [
    ...,
    "opensearch_xml",
    ...
  ]
  ```
+ Add "opensearch_xml" to URLS
  ```python
  from django.urls import path, include


  urlpatterns = [
    ...,
    path("opensearch/", include("opensearch_xml.urls")),
    ...
  ]
  ```

## Settings

Add OPENSEARCH_XML_\<params\> to the application settings

<dl>
    <dt>OPENSEARCH_XML_CONTACT_EMAIL = ""</dt>
    <dd>Email address of the maintainer the application</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_SHORT_NAME = ""</dt>
    <dd>Brief human-readable name of the search engine</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_DESCRIPTION = ""</dt>
    <dd>Human-readable description of the search engine and its contents</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_FAVICON_WIDTH = 16</dt>
    <dd>Width of the favicon</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_FAVICON_HEIGHT = 16</dt>
    <dd>Height of the favicon</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_FAVICON_TYPE = "image/x-icon"</dt>
    <dd>Type of the icon</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_FAVICON_FILE</dt>
    <dd>File on the favicon, relative to the path referenced in STATIC_PATH</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_SEARCH_URL = "search"</dt>
    <dd>Django URL name of the search. This URL will be passed to the `reverse()` function</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_SEARCH_QUERYSTRING = "q="</dt>
    <dd>Querystring used to prepend the search parameters</dd>
</dl>
<dl>
    <dt>OPENSEARCH_XML_INPUT_ENCODING = "UTF-8"</dt>
    <dd>Encoding for the querystring</dd>
</dl>

## Usage

Add the template tag `{% opensearch_xml_meta %}` into the page `<head>`.

```html
{% load opensearch_xml_tags %}
<html lang="en">
<head>
    <title>My title</title>
    ...
    {% opensearch_xml_meta %}
</head>
<body>
...
</body>
</html>
```
