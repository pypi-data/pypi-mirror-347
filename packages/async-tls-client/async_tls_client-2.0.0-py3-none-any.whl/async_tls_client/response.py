import base64
import json
from http.cookiejar import CookieJar
from typing import Union

from nocasedict import NocaseDict

from .cookies import cookiejar_from_dict


class Response:
    """object, which contains the response to an HTTP request."""

    def __init__(self):

        # Reference of URL the response is coming from (especially useful with redirects)
        self.url = None

        # Integer Code of responded HTTP Status, e.g. 404 or 200.
        self.status_code = self.status = None


        # String of responded HTTP Body.
        self.text = None

        # Case-insensitive Dictionary of Response Headers.
        self.headers = NocaseDict()

        # A CookieJar of Cookies the server sent back.
        self.cookies = cookiejar_from_dict({})

        self._content = False

    def __enter__(self):
        return self

    def __repr__(self):
        return f"<Response [{self.status_code}]>"

    def json(self, **kwargs):
        """parse response body to json (dict/list)"""
        return json.loads(self.text, **kwargs)

    @property
    def content(self):
        """Content of the response, in bytes."""

        if self._content is False:
            if self._content_consumed:
                raise RuntimeError("The content for this response was already consumed")

            if self.status_code == 0:
                self._content = None
            else:
                self._content = b"".join(self.iter_content(10 * 1024)) or b""
        self._content_consumed = True
        return self._content


def build_response(res: Union[dict, list], res_cookies: CookieJar) -> Response:
    """Builds a Response object """
    response = Response()
    # Add target / url
    response.url = res["target"]
    # Add status code
    response.status_code = response.status = res["status"]
    # Add headers
    response_headers = {}
    if res["headers"] is not None:
        for header_key, header_value in res["headers"].items():
            if len(header_value) == 1:
                response_headers[header_key] = header_value[0]
            else:
                response_headers[header_key] = header_value
    response.headers = response_headers
    # Add cookies
    response.cookies = res_cookies

    # Decode the byte-response (base64 format)
    try:
        data_part = res["body"].split(',', 1)[1]
    except IndexError:
        import logging
        logging.warning("Invalid base64 response format")
        data_part = res["body"]

    # Add response body
    response.text = base64.b64decode(data_part).decode(errors='ignore')
    # Add response content (bytes)
    response._content = base64.b64decode(data_part)
    return response
