__author__ = 'g8y3e'

from common_cloudshell_api import CommonAPISession
from cloudshell_api import CloudShellAPISession

from collections import OrderedDict

import unittest

class TestCloudShellAPISession(unittest.TestCase):
    REQUEST_DATA = dict()

    @staticmethod
    def api_send_request_mock(object, method_name, request_str, request_headers):
        TestCloudShellAPISession.REQUEST_DATA[method_name] = request_str

        return '''<?xml version="1.0" encoding="utf-8"?>
            <Response CommandName="Logon" Success="true"
                xmlns="http://schemas.qualisystems.com/ResourceManagement/ApiCommandResult.xsd"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <ErrorCode>0</ErrorCode>
                <ResponseInfo xsi:type="LogonResponseInfo">
                    <Domain Name="Global" Description="A domain that includes all available resources" DomainId="dbaf480c-09f7-46d3-a2e2-e35d3e374a16"/>
                </ResponseInfo>
            </Response>
        '''

    def setUp(self):
        host = '127.0.0.1'
        username = 'admin'
        password = 'admin'
        domain = 'Global'

        self._method_ptr = CommonAPISession._sendRequest
        CommonAPISession._sendRequest = TestCloudShellAPISession.api_send_request_mock

        self.api_session = CloudShellAPISession(host, username, password, domain)

    def tearDown(self):
        CommonAPISession._sendRequest = self._method_ptr

    def _convertRequestStr(self, request_str):
        request_str = request_str.replace('\n', '')
        request_str = request_str.replace(' ', '')

        return request_str

# begin TEST


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True: # raised by sys.exit(True) when tests failed
            pass