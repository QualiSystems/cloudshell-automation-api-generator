#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
import unittest

from cloudshell_api import CloudShellAPISession, ResourceInfoDto, AttributeNameValue, NameValuePair, AppDetails, \
    Deployment, ScriptInput, Script, Installation, DefaultDeployment, ApiEditAppRequest, \
    ResourceAttributesUpdateRequest, DeployAppInput, UserUpdateRequest, SetConnectorRequest

LOGON_RESPONSE = """<?xml version="1.0" encoding="utf-8"?>
                    <Response CommandName="Logon" Success="true" xmlns="http://schemas.qualisystems.com/ResourceManagement/ApiCommandResult.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <ErrorCode>0</ErrorCode>
                    <ResponseInfo xsi:type="LogonResponseInfo">
                    <Domain Name="{domain}" Description="A domain that includes all available resources" DomainId="dbaf480c-09f7-46d3-a2e2-e35d3e374a16"/>
                    <User Name="{username}" IsAdmin="true" IsActive="true" IsDomainAdmin="true"/>
                    <Token Token="V4h6L7+R6EqOtZJRojp0Gg=="/></ResponseInfo>
                    </Response>
                 """

COMMAND_RESPONSE = """<?xml version="1.0" encoding="utf-8"?>
                      <Response CommandName="{method}" Success="true" xmlns="http://schemas.qualisystems.com/ResourceManagement/ApiCommandResult.xsd" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                      <ErrorCode>0</ErrorCode>
                      <ResponseInfo xsi:type="{method}ResponseInfo"></ResponseInfo>
                      </Response>
                   """


class TestCloudShellAPISession(unittest.TestCase):
    def setUp(self):
        super(TestCloudShellAPISession, self).setUp()
        self.username = "UserName"
        self.domain = "dbaf480c-09f7-46d3-a2e2-e35d3e374a16"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = LOGON_RESPONSE.format(username=self.username, domain=self.domain)
            self.api_session = CloudShellAPISession(host="localhost",
                                                    username=self.username,
                                                    password="Password",
                                                    domain="Domain")

    def tearDown(self):
        super(TestCloudShellAPISession, self).tearDown()
        del self.api_session

    def test_create_resource(self):
        """  """

        method = "CreateResource"
        message = "<CreateResource>" \
                      "<resourceFamily>resourceFamily</resourceFamily>" \
                      "<resourceModel>resourceModel</resourceModel>" \
                      "<resourceName>resourceName</resourceName>" \
                      "<resourceAddress>resourceAddress</resourceAddress>" \
                      "<folderFullPath>folderFullPath</folderFullPath>" \
                      "<parentResourceFullPath>parentResourceFullPath</parentResourceFullPath>" \
                      "<resourceDescription>resourceDescription</resourceDescription>" \
                  "</CreateResource>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.CreateResource(resourceFamily="resourceFamily",
                                            resourceModel="resourceModel",
                                            resourceName="resourceName",
                                            resourceAddress="resourceAddress",
                                            folderFullPath="folderFullPath",
                                            parentResourceFullPath="parentResourceFullPath",
                                            resourceDescription="resourceDescription")

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_create_resources(self):
        """  """

        method = "CreateResources"
        message = "<CreateResources>" \
                      "<resourceInfoDtos>" \
                          "<ResourceInfoDto>" \
                              "<Address>127.0.0.1</Address>" \
                              "<Description>Resource Description 1</Description>" \
                              "<Family>Family_1</Family>" \
                              "<FolderFullpath>FolderFullpath_1</FolderFullpath>" \
                              "<FullName>Resource_FullName_1</FullName>" \
                              "<Model>Model_1</Model>" \
                              "<ParentFullName>ParentFullName_1</ParentFullName>" \
                          "</ResourceInfoDto>" \
                          "<ResourceInfoDto>" \
                              "<Address>127.0.0.2</Address>" \
                              "<Description>Resource Description 2</Description>" \
                              "<Family>Family_2</Family>" \
                              "<FolderFullpath>FolderFullpath_2</FolderFullpath>" \
                              "<FullName>Resource_FullName_2</FullName>" \
                              "<Model>Model_2</Model>" \
                              "<ParentFullName>ParentFullName_2</ParentFullName>" \
                          "</ResourceInfoDto>" \
                      "</resourceInfoDtos>" \
                  "</CreateResources>"

        res1 = ResourceInfoDto(Family="Family_1",
                               Model="Model_1",
                               FullName="Resource_FullName_1",
                               Address="127.0.0.1",
                               FolderFullpath="FolderFullpath_1",
                               ParentFullName="ParentFullName_1",
                               Description="Resource Description 1")

        res2 = ResourceInfoDto(Family="Family_2",
                               Model="Model_2",
                               FullName="Resource_FullName_2",
                               Address="127.0.0.2",
                               FolderFullpath="FolderFullpath_2",
                               ParentFullName="ParentFullName_2",
                               Description="Resource Description 2")

        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.CreateResources([res1, res2])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_find_resources(self):
        """  """

        method = "FindResources"
        message = "<FindResources>" \
                      "<resourceFamily>resourceFamily</resourceFamily>" \
                      "<resourceModel>resourceModel</resourceModel>" \
                      "<attributeValues>" \
                          "<AttributeNameValue>" \
                              "<Name>Attribute_Name</Name>" \
                              "<Value>Attribute_Value</Value>" \
                          "</AttributeNameValue>" \
                      "</attributeValues>" \
                      "<showAllDomains>false</showAllDomains>" \
                      "<resourceFullName>resourceFullName</resourceFullName>" \
                      "<exactName>true</exactName>" \
                      "<includeSubResources>true</includeSubResources>" \
                      "<resourceAddress>127.0.0.1</resourceAddress>" \
                      "<resourceUniqueIdentifier>resourceUniqueIdentifier</resourceUniqueIdentifier>" \
                      "<maxResults>500</maxResults>" \
                  "</FindResources>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.FindResources('resourceFamily', 'resourceModel',
                                           [AttributeNameValue("Attribute_Name", "Attribute_Value")], False,
                                           'resourceFullName', True, True, '127.0.0.1', 'resourceUniqueIdentifier', 500)

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_edit_apps_in_reservation(self):
        """  """

        method = "EditAppsInReservation"
        message = "<EditAppsInReservation>" \
                      "<reservationId>some_reservation_id</reservationId>" \
                      "<editAppsRequests>" \
                          "<ApiEditAppRequest>" \
                              "<AppDetails>" \
                                  "<Attributes>" \
                                      "<NameValuePair>" \
                                          "<Name>AttributeName1</Name>" \
                                          "<Value>AttributeValue1</Value>" \
                                      "</NameValuePair>" \
                                  "</Attributes>" \
                                  "<Driver>AppDriver</Driver>" \
                                  "<ModelName>AppModelName</ModelName>" \
                              "</AppDetails>" \
                              "<DefaultDeployment>" \
                                  "<Deployment>" \
                                      "<Attributes>" \
                                          "<NameValuePair>" \
                                              "<Name>AttributeName2</Name>" \
                                              "<Value>AttributeValue2</Value>" \
                                          "</NameValuePair>" \
                                      "</Attributes>" \
                                  "</Deployment>" \
                                  "<Installation>" \
                                      "<Attributes>" \
                                          "<NameValuePair>" \
                                              "<Name>AttributeName3</Name>" \
                                              "<Value>AttributeValue3</Value>" \
                                          "</NameValuePair>" \
                                      "</Attributes>" \
                                      "<Script>" \
                                          "<Inputs>" \
                                              "<ScriptInput>" \
                                                  "<Name>Script_Input_Name</Name>" \
                                                  "<Value>Script_Input_Value</Value>" \
                                              "</ScriptInput>" \
                                          "</Inputs>" \
                                          "<Name>Script_Name</Name>" \
                                      "</Script>" \
                                  "</Installation>" \
                                  "<Name>DeploymentName</Name>" \
                              "</DefaultDeployment>" \
                              "<Description>Description</Description>" \
                              "<Name>Name</Name>" \
                              "<NewName>NewName</NewName>" \
                          "</ApiEditAppRequest>" \
                      "</editAppsRequests>" \
                  "</EditAppsInReservation>"

        attribute1 = NameValuePair("AttributeName1", "AttributeValue1")
        app_details = AppDetails("AppModelName", [attribute1], "AppDriver")

        attribute2 = NameValuePair("AttributeName2", "AttributeValue2")
        deployment = Deployment([attribute2])

        attribute3 = NameValuePair("AttributeName3", "AttributeValue3")
        script_input = ScriptInput("Script_Input_Name", "Script_Input_Value")
        script = Script("Script_Name", [script_input])
        installation = Installation([attribute3], script)
        default_deployment = DefaultDeployment("DeploymentName", deployment, installation)
        app_request = ApiEditAppRequest("Name", "NewName", "Description", app_details, default_deployment)

        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.EditAppsInReservation("some_reservation_id", [app_request])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_get_resource_details(self):
        """  """

        method = "GetResourceDetails"
        message = "<GetResourceDetails>" \
                      "<resourceFullPath>resourceFullPath</resourceFullPath>" \
                      "<showAllDomains>false</showAllDomains>" \
                  "</GetResourceDetails>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.GetResourceDetails("resourceFullPath")

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_set_attributes_values(self):
        """  """

        method = "SetAttributesValues"
        message = "<SetAttributesValues>" \
                      "<resourcesAttributesUpdateRequests><ResourceAttributesUpdateRequest>" \
                      "<AttributeNamesValues>" \
                          "<AttributeNameValue>" \
                              "<Name>Attribute_Name</Name>" \
                              "<Value>Attribute_Value</Value>" \
                          "</AttributeNameValue>" \
                      "</AttributeNamesValues>" \
                      "<ResourceFullName>ResourceFullName</ResourceFullName>" \
                      "</ResourceAttributesUpdateRequest>" \
                      "</resourcesAttributesUpdateRequests>" \
                  "</SetAttributesValues>"

        update_request = ResourceAttributesUpdateRequest("ResourceFullName",
                                                         [AttributeNameValue("Attribute_Name", "Attribute_Value")])
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.SetAttributesValues([update_request])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_update_physical_connection(self):
        """  """

        method = "UpdatePhysicalConnection"
        message = "<UpdatePhysicalConnection>" \
                      "<resourceAFullPath>resourceAFullPath</resourceAFullPath>" \
                      "<resourceBFullPath>resourceBFullPath</resourceBFullPath>" \
                      "<overrideExistingConnections>true</overrideExistingConnections>" \
                  "</UpdatePhysicalConnection>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.UpdatePhysicalConnection("resourceAFullPath", "resourceBFullPath", True)

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_set_connector_attributes(self):
        """  """

        method = "SetConnectorAttributes"
        message = "<SetConnectorAttributes>" \
                      "<reservationId>reservationId</reservationId>" \
                      "<sourceResourceFullName>sourceResourceFullName</sourceResourceFullName>" \
                      "<targetResourceFullName>targetResourceFullName</targetResourceFullName>" \
                      "<attributeRequests>" \
                          "<AttributeNameValue>" \
                              "<Name>Attribute_Name</Name>" \
                              "<Value>Attribute_Value</Value>" \
                          "</AttributeNameValue>" \
                      "</attributeRequests>" \
                  "</SetConnectorAttributes>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.SetConnectorAttributes("reservationId",
                                                    "sourceResourceFullName",
                                                    "targetResourceFullName",
                                                    [AttributeNameValue("Attribute_Name", "Attribute_Value")])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_set_connector_attributes_via_alias(self):
        """  """

        method = "SetConnectorAttributesViaAlias"
        message = "<SetConnectorAttributesViaAlias>" \
                      "<reservationId>reservationId</reservationId>" \
                      "<connectorAlias>connectorAlias</connectorAlias>" \
                      "<attributeRequests>" \
                          "<AttributeNameValue>" \
                              "<Name>Attribute_Name</Name>" \
                              "<Value>Attribute_Value</Value>" \
                          "</AttributeNameValue>" \
                      "</attributeRequests>" \
                  "</SetConnectorAttributesViaAlias>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.SetConnectorAttributesViaAlias("reservationId",
                                                            "connectorAlias",
                                                            [AttributeNameValue("Attribute_Name", "Attribute_Value")])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_add_service_to_reservation(self):
        """  """

        method = "AddServiceToReservation"
        message = "<AddServiceToReservation>" \
                      "<reservationId>reservationId</reservationId>" \
                      "<serviceName>serviceName</serviceName>" \
                      "<alias>alias</alias>" \
                      "<attributes>" \
                          "<AttributeNameValue>" \
                              "<Name>Attribute_Name</Name>" \
                              "<Value>Attribute_Value</Value>" \
                          "</AttributeNameValue>" \
                      "</attributes>" \
                  "</AddServiceToReservation>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.AddServiceToReservation("reservationId",
                                                     "serviceName",
                                                     "alias",
                                                     [AttributeNameValue("Attribute_Name", "Attribute_Value")])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_set_service_attributes_values(self):
        """  """

        method = "SetServiceAttributesValues"
        message = "<SetServiceAttributesValues>" \
                      "<reservationId>reservationId</reservationId>" \
                      "<serviceAlias>serviceAlias</serviceAlias>" \
                      "<attributeRequests>" \
                          "<AttributeNameValue>" \
                              "<Name>Attribute_Name</Name>" \
                              "<Value>Attribute_Value</Value>" \
                          "</AttributeNameValue>" \
                      "</attributeRequests>" \
                  "</SetServiceAttributesValues>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.SetServiceAttributesValues("reservationId",
                                                        "serviceAlias",
                                                        [AttributeNameValue("Attribute_Name", "Attribute_Value")])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_deploy_app_to_cloud_provider_bulk(self):
        """  """

        method = "DeployAppToCloudProviderBulk"
        message = "<DeployAppToCloudProviderBulk>" \
                      "<reservationId>reservationId</reservationId>" \
                      "<appNames>" \
                          "<string>AppName_element</string>" \
                      "</appNames>" \
                      "<commandInputs>" \
                          "<DeployAppInput>" \
                              "<AppName>AppName</AppName>" \
                              "<Name>Name</Name>" \
                              "<Value>Value</Value>" \
                          "</DeployAppInput>" \
                      "</commandInputs>" \
                      "<printOutput>false</printOutput>" \
                  "</DeployAppToCloudProviderBulk>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.DeployAppToCloudProviderBulk("reservationId",
                                                          ["AppName_element"],
                                                          [DeployAppInput("AppName", "Name", "Value")],
                                                          False)

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_update_users_limitations(self):
        """  """

        method = "UpdateUsersLimitations"
        message = "<UpdateUsersLimitations>" \
                      "<userUpdateRequests>" \
                          "<UserUpdateRequest>" \
                              "<MaxConcurrentReservations>MaxConcurrentReservations</MaxConcurrentReservations>" \
                              "<MaxReservationDuration>MaxReservationDuration</MaxReservationDuration>" \
                              "<Username>Username</Username>" \
                          "</UserUpdateRequest>" \
                      "</userUpdateRequests>" \
                  "</UpdateUsersLimitations>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.UpdateUsersLimitations([UserUpdateRequest("Username",
                                                                       "MaxConcurrentReservations",
                                                                       "MaxReservationDuration")])

        send_request.assert_called_once_with(self.username, self.domain, method, message)

    def test_set_connectors_in_reservation(self):
        """  """

        method = "SetConnectorsInReservation"
        message = "<SetConnectorsInReservation>" \
                      "<reservationId>reservationId</reservationId>" \
                      "<connectors>" \
                          "<SetConnectorRequest>" \
                              "<Alias>Alias</Alias>" \
                              "<Direction>Direction</Direction>" \
                              "<SourceResourceFullName>SourceResourceFullName</SourceResourceFullName>" \
                              "<TargetResourceFullName>TargetResourceFullName</TargetResourceFullName>" \
                          "</SetConnectorRequest>" \
                      "</connectors>" \
                  "</SetConnectorsInReservation>"
        with mock.patch("cloudshell_api.CloudShellAPISession._sendRequest") as send_request:
            send_request.return_value = COMMAND_RESPONSE.format(method=method)
            self.api_session.SetConnectorsInReservation("reservationId",
                                                        [SetConnectorRequest("SourceResourceFullName",
                                                                             "TargetResourceFullName",
                                                                             "Direction",
                                                                             "Alias")])

        send_request.assert_called_once_with(self.username, self.domain, method, message)
