# encoding=utf8
__author__ = 'g8y3e'

import socket

from common_cloudshell_api import CommonAPISession
from common_cloudshell_api import CommonResponseInfo
from common_cloudshell_api import CommonAPIRequest

from collections import OrderedDict

# begin request class
# begin response class
class CloudShellAPISession(CommonAPISession):
    def __init__(self, host, username='', password='', domain='', timezone='UTC', datetimeformat='MM/dd/yyyy HH:mm',
                 port=8029, uri='/ResourceManagerApiService/'):
        CommonAPISession.__init__(self, host, username, password, domain)

        self.port = str(port)
        self.hostname = socket.gethostname() + ':' + self.port
        self.url = 'http://' + host + ':' + self.port + uri
        self.headers = {
            'Content-Type': 'text/xml',
            'Accept': '*/*',
            'ClientTimeZoneId': timezone,
            'DateTimeFormat': datetimeformat
        }

        self._encodeHeaders()
        response_info = self.Logon(username, password, domain)

        self.domain = response_info.Domain.DomainId

    def _sendRequest(self, username, domain, operation, message):
        request_headers = self.headers.copy()

        request_headers['Content-Length'] = len(message)
        request_headers['Host'] = self.host + ':' + self.port

        request_headers['Authorization'] = 'Username=' + username + \
                                           ';MachineName=' + self.hostname + \
                                           ';LoggedInDomainId=' + domain

        return CommonAPISession._sendRequest(self, operation, message, request_headers)

# begin API