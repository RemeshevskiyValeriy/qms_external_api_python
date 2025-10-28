import json
from typing import Any, Dict, Optional

from qgis.core import QgsNetworkAccessManager
from qgis.PyQt.QtCore import QUrl, QUrlQuery
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest

from .api_abstract import ApiClient, QmsNews
from .qt_network_error import QtNetworkError


class QgsApiClient(ApiClient):
    def _get_json(self, url, params=None):
        return json.loads(self._get_content(url, params).decode("utf-8"))

    def _get_content(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        Perform a blocking network GET request and return the raw content.

        :param url: The full URL to request.
        :type url: str
        :param params: Optional dictionary of query parameters to append to the URL.
        :type params: Optional[Dict[str, Any]]

        :return: The raw response content as bytes.
        :rtype: bytes
        :raises ConnectionError: If the network request fails with any QtNetworkError.
        """
        qurl_query = QUrlQuery()
        params = {} if params is None else params
        for key, value in params.items():
            qurl_query.addQueryItem(str(key), str(value))
        qurl = QUrl(url)
        qurl.setQuery(qurl_query)

        request = QNetworkRequest(qurl)
        response = QgsNetworkAccessManager.instance().blockingGet(request)

        if response.error() != QNetworkReply.NetworkError.NoError:
            error = QtNetworkError.from_qt(response.error())
            error_code = error.value.code
            message = error.value.description if error is not None else ""
            raise ConnectionError(error_code, message)

        return response.content().data()
