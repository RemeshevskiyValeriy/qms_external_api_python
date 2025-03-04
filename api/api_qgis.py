import json

from qgis.core import QgsNetworkAccessManager
from qgis.PyQt.QtCore import QUrl, QUrlQuery
from qgis.PyQt.QtNetwork import QNetworkReply, QNetworkRequest

from .api_abstract import ApiClient, QmsNews
from .qt_network_error import QtNetworkError


class QgsApiClient(ApiClient):
    def _get_json(self, url, params=None):
        return json.loads(self._get_content(url, params).decode("utf-8"))

    def _get_content(self, url, params=None):
        qurl_query = QUrlQuery()
        params = {} if params is None else params
        for key, value in params.items():
            qurl_query.addQueryItem(str(key), str(value))
        qurl = QUrl(url)
        qurl.setQuery(qurl_query)

        request = QNetworkRequest(qurl)
        response = QgsNetworkAccessManager.instance().blockingGet(request)

        if response.error() != QNetworkReply.NetworkError.NoError:
            error = QtNetworkError.from_int(response.error())
            message = error.value.description if error is not None else ""
            raise ConnectionError(message)

        return response.content().data()
