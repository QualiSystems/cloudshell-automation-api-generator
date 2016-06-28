#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Purpose: 
Created: 28.06.2016
Author:  Aleksey Bogoslovskyi
"""

from collections import OrderedDict
from common_cloudshell_api import CommonAPISession
from cloudshell_api import CloudShellAPISession

class TestCloudShellAPISession():
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

    def test_ActivateTopology(self):
        expect_request_str = '''
              <ActivateTopology>
              <reservationId>{reservationId}</reservationId>
              <topologyFullPath>{topologyFullPath}</topologyFullPath>
              </ActivateTopology>
            '''
        expect_str = self._convertRequestStr(expect_request_str)

        self.api_session.ActivateTopology(reservationId='{reservationId}', topologyFullPath='{topologyFullPath}')

        # self.assertTrue('ActivateTopology' in TestCloudShellAPISession.REQUEST_DATA)
        received_str = self._convertRequestStr(TestCloudShellAPISession.REQUEST_DATA['ActivateTopology'])
        # self.assertEqual(expect_str, received_str)

        TestCloudShellAPISession.REQUEST_DATA.pop('ActivateTopology', None)

    def test_ExecuteEnvironmentCommand(self):
        expect_request_str = '''
              <ExecuteEnvironmentCommand>
              <reservationId>{reservationId}</reservationId>
              <commandName>{commandName}</commandName>
              <commandInputs>
                <InputNameValue>
                  <Name>{Name}</Name>
                  <Value>{Value}</Value>
                </InputNameValue>
              </commandInputs>
              <printOutput>{printOutput}</printOutput>
              </ExecuteEnvironmentCommand>
            '''
        expect_str = self._convertRequestStr(expect_request_str)

        app_details =
        self.api_session.ExecuteEnvironmentCommand(reservationId='{reservationId}', commandName='{commandName}', commandInputs=[OrderedDict([('__name__', 'InputNameValue'), ('Name', '{Name}'), ('Value', '{Value}')])], printOutput='{printOutput}')

        # self.assertTrue('ExecuteEnvironmentCommand' in TestCloudShellAPISession.REQUEST_DATA)
        received_str = self._convertRequestStr(TestCloudShellAPISession.REQUEST_DATA['ExecuteEnvironmentCommand'])
        # self.assertEqual(expect_str, received_str)

        TestCloudShellAPISession.REQUEST_DATA.pop('ExecuteEnvironmentCommand', None)

    def test_EditAppsInReservation(self):
        expect_request_str = '''
<EditAppsInReservation>
<reservationId>{reservationId}</reservationId>
<editAppsRequests>
<ApiEditAppRequest>
<Name>{Name}</Name>
<NewName>{NewName}</NewName>
<Description>{Description}</Description>
<AppDetails>
  <ModelName>{ModelName}</ModelName>
  <Attributes>
    <NameValuePair>
      <Name>{Name}</Name>
      <Value>{Value}</Value>
    </NameValuePair>
  </Attributes>
  <Driver>{Driver}</Driver>
</AppDetails>
<DefaultDeployment>
  <Name>{Name}</Name>
  <Deployment>
    <Attributes>
      <NameValuePair>
        <Name>{Name}</Name>
        <Value>{Name}</Value>
      </NameValuePair>
    </Attributes>
  </Deployment>
  <Installation>
    <Attributes>
      <NameValuePair>
        <Name>{Name}</Name>
        <Value>{Name}</Value>
      </NameValuePair>
    </Attributes>
    <Script>
      <Name>{Name}</Name>
      <Inputs>
        <ScriptInput>
          <Name>{Name}</Name>
          <Value>{Value}</Value>
        </ScriptInput>
      </Inputs>
    </Script>
  </Installation>
</DefaultDeployment>
</ApiEditAppRequest>
</editAppsRequests>
</EditAppsInReservation>
            '''
        expect_str = self._convertRequestStr(expect_request_str)

        self.api_session.ExecuteEnvironmentCommand(reservationId='{reservationId}',
                                                   editAppsRequests=[OrderedDict([('__name__', 'editAppsRequests'), ('Name', '{Name}'), ('Value', '{Value}')])], printOutput='{printOutput}')

        # self.assertTrue('ExecuteEnvironmentCommand' in TestCloudShellAPISession.REQUEST_DATA)
        received_str = self._convertRequestStr(TestCloudShellAPISession.REQUEST_DATA['ExecuteEnvironmentCommand'])
        # self.assertEqual(expect_str, received_str)

        TestCloudShellAPISession.REQUEST_DATA.pop('ExecuteEnvironmentCommand', None)



if __name__ == "__main__":
    test = TestCloudShellAPISession()
    test.setUp()
    # test.test_ActivateTopology()
    test.test_ExecuteEnvironmentCommand()
    test.tearDown()
