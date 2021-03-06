from cloudshell.api.cloudshell_api import CloudShellAPISession
import os
import json

def get_user_param(parameter):
    """
    Returns a user param which is automaticlaly passed to the script
    as an environment variable
    :param str parameter: The name of the user parameter
    :rtype: str
    """
    return os.environ[parameter.upper()]


def get_api_session():
    """
    A shortcut to get an API session based on the built in env. variables
    :rtype: CloudShellAPISession
    """
    con_details = get_connectivity_context_details_dict()
    env_details = get_reservation_context_details_dict()
    return CloudShellAPISession(con_details['serverAddress'],
                                con_details['adminUser'],
                                con_details['adminPass'],
                                env_details['domain'])


def get_reservation_context_details_dict():
    """
    Get the reservation details dictionary for this execution
    These details are automatically passed to the driver by CloudShell
    :rtype: dict[str,str]
    """
    return _get_quali_env_variable_object('reservationContext')


def get_resource_context_details_dict():
    """
    Get the resource details dictionary for this execution
    These details are automatically passed to the driver by CloudShell
    :rtype: dict[str,str]
    """
    return _get_quali_env_variable_object('resourceContext')


def get_reservation_context_details():
    """
    Get the reservation details for this execution
    These details are automatically passed to the driver by CloudShell

    :rtype: ReservationContextDetails
    """
    res_dict = get_reservation_context_details_dict()
    env_params = EnvironmentParameters(get_global_inputs(),
                                       get_resource_requirement_inputs(),
                                       get_resource_additional_info_inputs())
    res_details = ReservationContextDetails(res_dict['environmentName'],
                                            res_dict['domain'],
                                            res_dict['description'],
                                            env_params,
                                            res_dict['ownerUser'],
                                            res_dict['ownerPass'],
                                            res_dict['id'])
    return res_details


def get_resource_context_details():
    """
    Get the resource details dictionary for this execution
    These details are automatically passed to the driver by CloudShell

    :rtype: ResourceContextDetails
    """
    res_dict = get_resource_context_details_dict()
    res_details = ResourceContextDetails(res_dict['name'],
                                         res_dict['address'],
                                         res_dict['model'],
                                         res_dict['family'],
                                         res_dict['description'],
                                         res_dict['fullname'],
                                         res_dict['attributes'])
    return res_details


def get_connectivity_context_details_dict():
    """
    Get the connectivity details dictionary for this execution
    :rtype: dict[str,str]
    """
    return _get_quali_env_variable_object('qualiConnectivityContext')


def get_connectivity_context_details():
    """
    Get the connectivity details dictionary for this execution
    :rtype: ConnectivityContextDetails
    """
    con_dict = get_connectivity_context_details_dict()
    return ConnectivityContextDetails(con_dict['serverAddress'],
                                      con_dict['tsAPIPort'],
                                      con_dict['adminUser'],
                                      con_dict['adminPass'])


def get_global_inputs():
    """
    Get the global inputs dictionary for the current reservation
    :rtype: dict[str,str]
    """
    reservationParams = get_reservation_context_details_dict()['parameters']
    return _covert_to_python_dictionary(reservationParams['globalInputs'])


def get_resource_requirement_inputs():
    """
    Get the resource requirements inputs dictionary
    :rtype: ResourceInputs
    """
    reservationParams = get_reservation_context_details_dict()['parameters']
    return _covert_to_resource_inputs_dictionary(
        reservationParams['resourceRequirements'])


def get_resource_additional_info_inputs():
    """
    Get the resource additional inputs inputs dictionary
    :rtype: ResourceInputs
    """
    reservationParams = get_reservation_context_details_dict()['parameters']
    return _covert_to_resource_inputs_dictionary(
        reservationParams['resourceAdditionalInfo'])


def _get_quali_env_variable_object(name):
    json_string = os.environ[name]
    json_object = json.loads(json_string)
    return json_object


def _get_quali_env_variable_as_string(name):
    return json.dumps(_get_quali_env_variable_object(name))


def _covert_to_python_dictionary(parameters):
    inputsDictionary = {}
    for param in parameters:
        inputsDictionary[param['parameterName']] = param['value']
    return inputsDictionary


def _covert_to_resource_inputs_dictionary(parameters):
    inputsDictionary = ResourceInputs()
    for param in parameters:
        resource_name = param['resourceName']
        value = param['value']
        param_name = param['parameterName']
        possible_values = param.get('possibleValues', None)
        data = ResourceInputData(resource_name, param_name, value,
                                 possible_values)
        inputsDictionary[resource_name] = data
    return inputsDictionary


class ConnectivityContextDetails:
    def __init__(self, server_address, cloudshell_api_port,
                 admin_user, admin_pass):
        self.server_address = server_address
        """:type : str"""
        self.cloudshell_api_port = cloudshell_api_port
        """:type : str"""
        self.admin_user = admin_user
        """:type : str"""
        self.admin_pass = admin_pass
        """:type : str"""


class ResourceContextDetails:
    def __init__(self, name, address, model,family,
                 description, fullname, attributes):
        self.name = name
        """:type : str"""
        self.address = address
        """:type : str"""
        self.model = model
        """:type : str"""
        self.family = family
        """:type : str"""
        self.description = description
        """:type : str"""
        self.fullname = fullname
        """:type : str"""
        self.attributes = attributes
        """:type : dict[str,str]"""


class ReservationContextDetails:
    def __init__(self, environment_name, domain, description,
                 parameters, owner_user, owner_password, reservation_id):
        self.environment_name = environment_name
        """:type : str"""
        self.domain = domain
        """:type : str"""
        self.description = description
        """:type : str"""
        self.parameters = parameters
        """:type : EnvironmentParameters"""
        self.owner_user = owner_user
        """:type : str"""
        self.owner_password = owner_password
        """:type : str"""
        self.id = reservation_id
        """:type : str"""


class EnvironmentParameters:
    def __init__(self, global_inputs, resource_requirements,
                 resource_additional_info):
        self.global_inputs = global_inputs
        """:type : dict[str,str]"""
        self.resource_requirements = resource_requirements
        """:type : ResourceInputs"""
        self.resource_additional_info = resource_additional_info
        """:type : ResourceInputs"""


class ResourceInputData:
    def __init__(self, resource_name, param_name, value, possible_values):
        self.resource_name = resource_name
        """:type : str"""
        self.value = value
        """:type : str"""
        self.possible_values = possible_values
        """:type : list[str]"""
        self.param_name = param_name
        """:type : str"""


class ResourceInputs:
    dictionary = {}
    """:type : dict[str, dict[str, ResourceInputData]]"""

    def __getitem__(self, resource_name):
        """:rtype: dict[str, dict[str, ResourceInputData]]"""
        return self.dictionary[resource_name]

    def __setitem__(self, resource_name, resource_input_data):
        if resource_name not in self.dictionary.keys():
            self.dictionary[resource_name] = {}
        self.dictionary[resource_name][resource_input_data.param_name]\
            = resource_input_data
