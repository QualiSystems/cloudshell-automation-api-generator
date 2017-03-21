# encoding=utf8
__author__ = 'g8y3e'

import socket
import base64

from common_cloudshell_api import CommonAPISession
from common_cloudshell_api import CommonResponseInfo
from common_cloudshell_api import CommonAPIRequest

from collections import OrderedDict

# begin request class
# begin response class

class ApiEditAppRequest(CommonAPIRequest):
    def __init__(self, Name, NewName, Description, AppDetails, DefaultDeployment):
        """
            :param str Name: constructor parameter
            :param str NewName: constructor parameter
            :param str Description: constructor parameter
            :param AppDetails AppDetails: constructor parameter
            :param DefaultDeployment DefaultDeployment: constructor parameter
        """
        CommonAPIRequest.__init__(self, Name=Name, NewName=NewName, Description=Description, AppDetails=AppDetails,
                                  DefaultDeployment=DefaultDeployment)


class AppDetails(CommonAPIRequest):
    def __init__(self, ModelName, Attributes, Driver):
        """
            :param str ModelName: constructor parameter
            :param list[NameValuePair] Attributes: constructor parameter
            :param str Driver: constructor parameter
        """
        CommonAPIRequest.__init__(self, ModelName=ModelName, Attributes=Attributes, Driver=Driver)


class NameValuePair(CommonAPIRequest):
    def __init__(self, Name, Value):
        """
            :param str Name: constructor parameter
            :param str Value: constructor parameter
        """
        CommonAPIRequest.__init__(self, Name=Name, Value=Value)


class DefaultDeployment(CommonAPIRequest):
    def __init__(self, Name, Deployment, Installation):
        """
            :param str Name: constructor parameter
            :param Deployment Deployment: constructor parameter
            :param Installation Installation: constructor parameter
        """
        CommonAPIRequest.__init__(self, Name=Name, Deployment=Deployment, Installation=Installation)


class Deployment(CommonAPIRequest):
    def __init__(self, Attributes):
        """
            :param list[NameValuePair] Attributes: constructor parameter
        """
        CommonAPIRequest.__init__(self, Attributes=Attributes)


class Installation(CommonAPIRequest):
    def __init__(self, Attributes, Script):
        """
            :param list[NameValuePair] Attributes: constructor parameter
            :param Script Script: constructor parameter
        """
        CommonAPIRequest.__init__(self, Attributes=Attributes, Script=Script)


class Script(CommonAPIRequest):
    def __init__(self, Name, Inputs):
        """
            :param str Name: constructor parameter
            :param list[ScriptInput] Inputs: constructor parameter
        """
        CommonAPIRequest.__init__(self, Name=Name, Inputs=Inputs)


class ScriptInput(CommonAPIRequest):
    def __init__(self, Name, Value):
        """
            :param str Name: constructor parameter
            :param str Value: constructor parameter
        """
        CommonAPIRequest.__init__(self, Name=Name, Value=Value)


class CloudShellAPISession(CommonAPISession):
    def __init__(self, host, username='', password='', domain='', timezone='UTC', datetimeformat='MM/dd/yyyy HH:mm',
                 token_id='', port=8029, uri='/ResourceManagerApiService/'):
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

        self.token_id = token_id
        response_info = None
        if len(token_id) == 0:
            response_info = self.Logon(username, password, domain)
        else:
            response_info = self.SecureLogon(token_id, domain)

        self.domain = response_info.Domain.DomainId
        self.token_id = response_info.Token.Token

    def _sendRequest(self, username, domain, operation, message):
        request_headers = self.headers.copy()

        request_headers['Content-Length'] = len(message)
        request_headers['Host'] = self.host + ':' + self.port

        request_headers['Authorization'] = 'MachineName=' + self.hostname + \
                                           ';Token=' + self.token_id

        return CommonAPISession._sendRequest(self, operation, message, request_headers)

    def UpdateDriver(self, driverName='', driverFileName=''):
        """
            Updating driver in cloudshell

            :param driverName: str
            :param driverFile: str
            :param driverFileName: str
            :return: string
        """
        driverFile = open(driverFileName, 'rb').read()

        return self.generateAPIRequest(OrderedDict([('method_name', 'UpdateDriver'), ('driverName', driverName), ('driverFile', base64.b64encode(driverFile)),
                                                    ('driverFileName', driverFileName)]))

    def UpdateScript(self, scriptName='', scriptFileName=''):
        """
            Updating driver in cloudshell

            :param driverName: str
            :param driverFile: str
            :param driverFileName: str
            :return: string
        """
        scriptFile = open(scriptFileName, 'rb').read()

        return self.generateAPIRequest(OrderedDict([('method_name', 'UpdateScript'), ('scriptName', scriptName), ('scriptFile', base64.b64encode(scriptFile)),
                                                    ('scriptFileName', scriptFileName)]))

    def GetAppsDetailsInReservation(self, reservationId='', appNames=[]):
        """
            Retrieves information on the specified apps in the reservation.

            :param str reservationId: Specify the string that represents the reservation's unique identifier.
            :param list[str] appNames: Specify the apps names.

            :rtype: ReservationAppsResponseInfo
        """
        return self.generateAPIRequest(OrderedDict([('method_name', 'GetAppsDetailsInReservation'), ('reservationId', reservationId), ('appNames', appNames)]))

# begin API