__author__ = 'g8y3e'

import tarfile
import StringIO
import xml.etree.ElementTree as etree
from collections import OrderedDict

import os
import re
import codecs
import sys

class XMLWrapper:
    @staticmethod
    def parse_xml(xml_str, parser=None):
        return etree.fromstring(xml_str, parser)

    @staticmethod
    def parse_xml_from_file(xml_path):
        utf8_parser = etree.XMLParser(encoding='utf-8')
        xml_str = open(xml_path).read()
        return etree.fromstring(xml_str, parser=utf8_parser)

    @staticmethod
    def get_root_node(node):
        return node.getroot()

    @staticmethod
    def get_child_node(parent_node, child_name, find_prefix=''):
        return parent_node.find(find_prefix + child_name)

    @staticmethod
    def get_all_child_node(parent_node, child_name, find_prefix=''):
        return parent_node.findall(find_prefix + child_name)

    @staticmethod
    def get_child_node_by_attr(parent_node, child_name, attr_name, attr_value, find_prefix=''):
        return parent_node.find(find_prefix + child_name + '[@' + attr_name + '=\'' + attr_value + '\']')

    @staticmethod
    def get_all_child_node_by_attr(parent_node, child_name, attr_name, attr_value):
        return parent_node.findall(child_name + '[@' + attr_name + '=\'' + attr_value + '\']')

    @staticmethod
    def get_node_name(node):
        return node.tag

    @staticmethod
    def get_node_text(node):
        return node.text

    @staticmethod
    def get_node_attr_list(node):
        return node.keys()

    @staticmethod
    def get_node_attr(node, attribute_name, find_prefix=''):
        return node.get(find_prefix + attribute_name)

    @staticmethod
    def get_node_prefix(node, prefix_name):
        prefix = ''
        for attrib_name, value in node.attrib.items():
            if attrib_name[0] == "{":
                prefix, ignore, tag = attrib_name[1:].partition("}")
                return "{" + prefix + "}"

        if len(prefix) == 0:
            node_tag = node.tag
            if node_tag[0] == "{":
                prefix, ignore, tag = node_tag[1:].partition("}")
                return "{" + prefix + "}"

        return prefix

    @staticmethod
    def get_string_from_xml(node, pretty_print=False):
        return etree.to_string(node, pretty_print=pretty_print)

    @staticmethod
    def get_node_child_count(node):
        count = 0
        for child_node in node:
            count += 1

        return count

class GeneratorResource:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class CommandParameterInfo:
    def __init__(self, name, type, default_value, description):
        self.name = name
        self.type = type
        self.default_value = default_value

        self.description = description

class ResponseClassData:
    def __init__(self):
        self.object_attributes = dict()
        self.object_list_attributes = dict()
        self.object_comment_attributes = dict()

        self.parent_type = 'CommonResponseInfo'

    @staticmethod
    def _list_to_string(prefix, data_map, value_prefix='', value_postfix='', comment_postfix='',
                        comment_map=dict()):
        atrributes_data = ''
        count_fields = 0
        index = 0
        for key, value in data_map.items():
            count_fields += 1

            comment_type = ''
            if len(comment_postfix) > 0:
                if key in comment_map:
                    comment_type = comment_map[key]
                else:
                    comment_type = value

            atrributes_data += prefix + "self." + key + " = " + value_prefix + value + value_postfix + \
                               comment_type + comment_postfix + "\n"

        #if len(atrributes_data) != 0:
        #    atrributes_data = atrributes_data[:-1]

        return atrributes_data

    def to_string(self):
        attributes = ''

        attributes += self._list_to_string((' ' * 8), self.object_attributes, '', "\n" + (' ' * 8) +
                                           '""":type : ', '"""', self.object_comment_attributes)
        attributes += self._list_to_string((' ' * 8), self.object_list_attributes, "{'list': ", "}\n" + (' ' * 8) +
                                           '""":type : list[', ']"""', self.object_comment_attributes)

        return attributes

class CloudShellAPIGenerator:
    def __init__(self, api_documentation_path, api_response_path, version, api_methods_result,
                 output_folder, package_name, package_filename, package_root_folder,
                 is_debug):
        self.api_response_node = XMLWrapper.parse_xml_from_file(api_response_path)
        self.api_node = XMLWrapper.parse_xml_from_file(api_documentation_path)
        self.api_methods_result_node = XMLWrapper.parse_xml_from_file(api_methods_result)

        self.folder_prefix = output_folder + '/'
        self.resources = dict()
        self.script_helper_resources = dict()

        self._api_method_flag = '# begin API'
        self._api_response_class_flag = '# begin response class'
        self._api_request_class_flag = '# begin request class'

        self._test_api_flag = '# begin TEST'
        self._api_method_position = -1
        self._api_response_position = -1
        self._api_request_position = -1
        self._test_api_position = -1

        version_part = version.split('.')
        self._version = int(version_part[0])

        self._package_prefix = '/api/'
        self._helpers_prefix = '/helpers/'
        self._script_helpers_prefix = 'scripts/'


        self._package_name = package_name

        self._package_root_folder = package_root_folder

        self._package_version = version

        self._package_filename = package_filename + self._package_version
        self._is_debug = is_debug

        self._inserted_request_classes = dict()
        self._api_response_class_data = dict()

    def isSevenVersion(self):
        return (self._version >= 7)

        # def _read_resources(self):
        #     if not os.path.exists(self.folder_prefix):
        #         os.makedirs(self.folder_prefix)
    #
    #     self.api_method_template = StringIO(LoadResource(0, u'API_METHOD_TMP', 1)).read()
    #     self.api_response_class_template = StringIO(LoadResource(0, u'API_RESPONSE_TMP', 1)).read()
    #     self.test_api_method_template = StringIO(LoadResource(0, u'TEST_API_METHOD_TMP', 1)).read()
    #
    #     name = 'common_cloudshell_api.py'
    #     data = StringIO(LoadResource(0, u'COMMON_API', 1)).read()
    #     self.resources[name] = GeneratorResource(name, data)
    #
    #     name = 'cloudshell_api.py'
    #     if self.isSevenVersion():
    #         data = StringIO(LoadResource(0, u'API_V7', 1)).read()
    #     else:
    #         data = StringIO(LoadResource(0, u'API_V6', 1)).read()
    #     self.resources[name] = GeneratorResource(name, data)
    #
    #     name = 'test_cloudshell_api.py'
    #     data = StringIO(LoadResource(0, u'API_TEST', 1)).read()
    #     self.resources[name] = GeneratorResource(name, data)

    def _read_resources_not_exe(self):
        if not os.path.exists(self.folder_prefix):
            os.makedirs(self.folder_prefix)

        self.api_method_template = open('template/python/api/api_method_template').read()
        self.api_response_class_template = open('template/python/api/api_response_object_template').read()
        self.api_request_class_template = open('template/python/api/api_request_class_template').read()
        self.test_api_method_template = open('template/python/api/test_api_method_template').read()

        name = 'common_cloudshell_api.py'
        data = open('template/python/api/common_cloudshell_api.py').read()
        self.resources[name] = GeneratorResource(name, data)

        name = 'cloudshell_api.py'
        if self.isSevenVersion():
            data = open('template/python/api/cloudshell_api_v7.py').read()
        else:
            data = open('template/python/api/cloudshell_api_v6.py').read()
        self.resources[name] = GeneratorResource(name, data)

        if self._is_debug:
            name = 'test_cloudshell_api.py'
            data = open('template/python/api/test_cloudshell_api.py').read()
            self.resources[name] = GeneratorResource(name, data)

        self.package_resources = dict()

        if len(self._package_name) != 0:
            name = '__init__.py'
            self.resources[name] = GeneratorResource(name, "__author__ = 'g8y3e'\n")

            name = 'cloudshell_dev_helpers.py'
            data = open('template/python/api/cloudshell_dev_helpers.py').read()
            self.script_helper_resources[name] = GeneratorResource(name, data)

            name = 'cloudshell_scripts_helpers.py'
            data = open('template/python/api/cloudshell_scripts_helpers.py').read()
            self.script_helper_resources[name] = GeneratorResource(name, data)

            name = 'README.txt'
            data = open('template/python/package/README.txt').read()
            self.package_resources[name] = GeneratorResource(name, data)

            name = 'requirements.txt'
            data = open('template/python/package/requirements.txt').read()
            self.package_resources[name] = GeneratorResource(name, data)

            name = 'test_requirements.txt'
            data = open('template/python/package/test_requirements.txt').read()
            self.package_resources[name] = GeneratorResource(name, data)

            name = 'version.txt'
            data = open('template/python/package/version.txt').read()
            data = data.replace('<version>', self._package_version)
            self.package_resources[name] = GeneratorResource(name, data)

            name = 'setup.py'
            data = open('template/python/package/setup.py').read()
            self.package_resources[name] = GeneratorResource(name, data)

            setup_data = self.package_resources['setup.py'].data
            setup_data = setup_data.replace("<package_name>", self._package_name)
            self.package_resources['setup.py'].data = setup_data

    def _write_data(self, filename, data):
        file_stream = codecs.open(filename, 'w', 'utf-8')
        file_stream.write(data)
        file_stream.close()

    def _flush_data(self):
        for key, object in self.resources.items():
            self._write_data(self.folder_prefix + object.name, object.data)

        for key, object in self.package_resources.items():
            self._write_data(self.folder_prefix + object.name, object.data)

        for key, object in self.script_helper_resources.items():
            self._write_data(self.folder_prefix + object.name, object.data)

    def _pack_data(self):
        tar = tarfile.open(self.folder_prefix + self._package_filename + ".tar.gz", "w:gz")
        tarFolder = tarfile.TarInfo(self._package_root_folder + self._package_prefix)
        tarFolder.type = tarfile.DIRTYPE
        tar.addfile(tarFolder)
        for key in self.resources:
            tar.add(self.folder_prefix + key, arcname=self._package_root_folder + self._package_prefix + key)
        tar.add(self.folder_prefix + '__init__.py', arcname=self._package_root_folder + '/__init__.py')

        tarFolder = tarfile.TarInfo(self._package_root_folder + self._helpers_prefix)
        tarFolder.type = tarfile.DIRTYPE
        tar.addfile(tarFolder)
        tar.add(self.folder_prefix + '__init__.py', arcname=self._package_root_folder + self._helpers_prefix + '__init__.py')


        tarFolder = tarfile.TarInfo(self._package_root_folder + self._helpers_prefix + self._script_helpers_prefix)
        tarFolder.type = tarfile.DIRTYPE
        tar.addfile(tarFolder)
        tar.add(self.folder_prefix + '__init__.py', arcname=self._package_root_folder + self._helpers_prefix + self._script_helpers_prefix + '__init__.py')


        for key in self.script_helper_resources:
            tar.add(self.folder_prefix + key, arcname=self._package_root_folder + self._helpers_prefix + self._script_helpers_prefix + key)

        for key in self.package_resources:
            tar.add(self.folder_prefix + key, arcname=key)
        tar.close()

        for key in self.script_helper_resources:
            os.remove(self.folder_prefix + key)

        for key in self.resources:
            os.remove(self.folder_prefix + key)

        for key in self.package_resources:
            os.remove(self.folder_prefix + key)

    def _insert_api_method(self, method_data):
        api_data = self.resources['cloudshell_api.py'].data

        if self._api_method_position == -1:
            match_result = re.search(self._api_method_flag, api_data)
            if match_result is None:
                raise Exception('API Generator', "Can't find begin flag!")

            self._api_method_position = match_result.start()
            api_data = api_data[:self._api_method_position] + api_data[match_result.end() + 1:]

        api_data = api_data[:self._api_method_position] + method_data + api_data[self._api_method_position:]

        self._api_method_position += len(method_data)

        self.resources['cloudshell_api.py'].data = api_data

    def _insert_api_request_class(self, response_data):
        api_data = self.resources['cloudshell_api.py'].data

        if self._api_request_position == -1:
            match_result = re.search(self._api_request_class_flag, api_data)
            if match_result is None:
                raise Exception('API Generator', "Can't find begin flag!")

            self._api_request_position = match_result.start()
            api_data = api_data[:self._api_request_position] + api_data[match_result.end() + 1:]

        api_data = api_data[:self._api_request_position] + response_data + api_data[self._api_request_position:]

        self._api_request_position += len(response_data)

        self.resources['cloudshell_api.py'].data = api_data

    def _insert_api_response_class(self, response_data):
        api_data = self.resources['cloudshell_api.py'].data

        if self._api_response_position == -1:
            match_result = re.search(self._api_response_class_flag, api_data)
            if match_result is None:
                raise Exception('API Generator', "Can't find begin flag!")

            self._api_response_position = match_result.start()
            api_data = api_data[:self._api_response_position] + api_data[match_result.end() + 1:]

        api_data = api_data[:self._api_response_position] + response_data + api_data[self._api_response_position:]

        self._api_response_position += len(response_data)

        self.resources['cloudshell_api.py'].data = api_data

    def _get_api_method_parameter_type(self, request_node, param_name):
        param_node = XMLWrapper.get_child_node(request_node, param_name)

        for child_node in param_node:
            return XMLWrapper.get_node_name(child_node)

    def _append_api_method(self, name, description, arguments, request_xml):
        request_node = XMLWrapper.parse_xml(request_xml)

        api_method_data = self.api_method_template
        api_method_data = api_method_data.replace('<method_name>', name)

        # this is crutch
        method_name = name
        method_name = method_name.replace('CreateImmediateTopologyReservation', 'CreateImmediateReservation')
        method_name = method_name.replace('CreateTopologyReservation', 'CreateReservation')
        api_method_data = api_method_data.replace('<method_name_attr>', method_name)

        arguments_str = ''
        generic_arguments_str = ''
        description += '\n\n'
        for key, object in arguments.items():
            argument_type_str = ''

            if len(generic_arguments_str) == 0:
                generic_arguments_str = ', '

            if len(arguments_str) == 0:
                arguments_str += ', '

            arguments_str += key + '='
            if object.type == 'string':
                argument_type_str = 'str'
                if len(object.default_value) > 0:
                    arguments_str += '\'' + object.default_value + '\''
                else:
                    arguments_str += '\'\''
            elif object.type == 'string[]':
                type = self._get_api_method_parameter_type(request_node, key)
                if type == 'string':
                    type = 'str'
                argument_type_str = 'list[' + type + ']'
                arguments_str += '[]'
            elif object.type == 'string[,]':
                type = self._get_api_method_parameter_type(request_node, key)
                if type == 'string':
                    type = 'str'
                argument_type_str = 'list[' + type + ']'

                arguments_str += '[]'
            elif object.type == 'int' or object.type == 'double':
                if object.type == 'int':
                    argument_type_str = 'int'
                else:
                    argument_type_str = 'float'

                arguments_str += object.default_value
                if len(object.default_value) == 0:
                    arguments_str += '0'
            else:
                if object.default_value.lower() in ['true', 'false', 'yes', 'no', 'on', 'off']:
                    if object.default_value.lower() in ['true', 'yes', 'on']:
                        arguments_str += 'True'
                    else:
                        arguments_str += 'False'

                    argument_type_str = 'bool'
                else:
                    arguments_str += object.default_value
                    if len(object.default_value) == 0:
                        if object.type == 'shareability' or object.type == 'yesnooptions':
                            arguments_str += "False"
                            argument_type_str = 'bool'
                        elif object.type == 'baudrate':
                            arguments_str += "0"
                            argument_type_str = 'int'
                        else:
                            arguments_str += "''"
                            argument_type_str = 'str'

            if object.type == 'string[,]':
                generic_arguments_str += "('" + key + "', CommonAPIRequest.toContainer(" + key + "))"
            else:
                generic_arguments_str += "('" + key + "', " + key + ")"

            arguments_str += ', '
            generic_arguments_str += ', '

            description += (' ' * 12) + ':param ' + argument_type_str + ' ' + key + ': ' + object.description + '\n'

        result_type_node = XMLWrapper.get_child_node(self.api_methods_result_node, name)
        result_type = 'str'
        if result_type_node is not None:
            result_type = XMLWrapper.get_node_text(result_type_node)

        description += '\n' + (' ' * 12) + ':rtype: ' + result_type
        arguments_str = arguments_str[:-2]
        generic_arguments_str = generic_arguments_str[:-2]

        api_method_data = api_method_data.replace('<description>', description)
        api_method_data = api_method_data.replace('<arguments>', arguments_str)
        api_method_data = api_method_data.replace('<arguments_in_method>', generic_arguments_str)

        self._insert_api_method(api_method_data)

    def _parse_api_request_class(self, class_node):
        api_request_class_template = self.api_request_class_template

        class_name = XMLWrapper.get_node_name(class_node)

        if class_name in ('string', 'int'):
            return

        if class_name in self._inserted_request_classes:
            return

        self._inserted_request_classes[class_name] = class_name
        api_request_class_template = api_request_class_template.replace('<request_name>', class_name)
        arguments_str = ''
        arguments_in_method_str = ''
        comments_str = ''
        comment_prefix = (' ' * 12) + ':param '

        for child_parameters in class_node:
            parameter_name = XMLWrapper.get_node_name(child_parameters)
            arguments_str += parameter_name + ', '
            arguments_in_method_str += parameter_name + '=' + parameter_name + ', '

            parameter_type = 'str'
            for inner_param_node in child_parameters:
                parameter_type = 'list[' + XMLWrapper.get_node_name(inner_param_node) + ']'
                self._parse_api_request_class(inner_param_node)

            comments_str += comment_prefix + parameter_type + ' ' + parameter_name + ': constructor parameter\n'

        if len(arguments_str) >= 2:
            arguments_str = arguments_str[:-2]

        if len(arguments_in_method_str) >= 2:
            arguments_in_method_str = arguments_in_method_str[:-2]

        if len(comments_str) >= 1:
            comments_str = comments_str[:-1]

        api_request_class_template = api_request_class_template.replace('<args>', arguments_str)
        api_request_class_template = api_request_class_template.replace('<args_in_method>', arguments_in_method_str)
        api_request_class_template = api_request_class_template.replace('<comments>', comments_str)

        self._insert_api_request_class(api_request_class_template)

    def _append_api_request_class(self, request_method_name, command_params, request_xml):
        request_node = XMLWrapper.parse_xml(request_xml)

        for key, object in command_params.items():
            if object.type == 'string[,]':
                class_nodes = XMLWrapper.get_child_node(request_node, key)
                if class_nodes is None:
                    continue

                for child_class_node in class_nodes:
                    self._parse_api_request_class(child_class_node)

    def _get_node_mandatory_attribute(self, node, attribute_name):
        attribute_value = XMLWrapper.get_node_attr(node, attribute_name)
        if attribute_value is None:
            raise Exception('API Generator', "Response object don't have atrribute '" + attribute_name + "'!")

        return attribute_value

    def _add_attribute_data(self, response_data, class_name, attribute_name, attribute_type, container_type='object'):
        attribute_type = attribute_type.replace('xs:', '')
        attribute_type = attribute_type.replace('string', 'str')
        attribute_type = attribute_type.replace('boolean', 'bool')
        attribute_type = attribute_type.replace('double', 'float')

        response_data.object_comment_attributes[attribute_name] = attribute_type
        if class_name == attribute_type:
            attribute_type = 'object'

        if container_type == 'object':
            response_data.object_attributes[attribute_name] = attribute_type
        elif container_type == 'object_list':
            response_data.object_list_attributes[attribute_name] = attribute_type
        else:
            return False

        return True

    def _get_response_type_name(self, xs_prefix, name):
        type_node = XMLWrapper.get_child_node_by_attr(self.api_response_node, xs_prefix + 'simpleType', 'name', name)
        if type_node is not None:
            parent_type_node = XMLWrapper.get_child_node(type_node, 'restriction', xs_prefix)
            if parent_type_node is None:
                raise Exception('API Generator', 'Simple type need to has parent type!')

            type_name = XMLWrapper.get_node_attr(parent_type_node, 'base')
            if type_name is None:
                raise Exception('API Generator', 'Simple type need to has parent type!')

            return type_name
        else:
            return name

    def _parse_response_xsd_object(self, xs_prefix, node, parent_node, class_name, class_data_map, response_data=None):
        if class_name in class_data_map:
            return
        elif response_data is None:
            response_data = ResponseClassData()

        for child_node in node:
            node_name = XMLWrapper.get_node_name(child_node)
            if node_name == (xs_prefix + 'attribute'):
                attribute_name = self._get_node_mandatory_attribute(child_node, 'name')
                attribute_type = self._get_node_mandatory_attribute(child_node, 'type')
                attribute_type = self._get_response_type_name(xs_prefix, attribute_type)

                self._add_attribute_data(response_data, class_name, attribute_name, attribute_type)
            elif node_name == (xs_prefix + 'complexContent'):
                self._parse_response_xsd_object(xs_prefix, child_node, parent_node, class_name, class_data_map,
                                                response_data)
            elif node_name == (xs_prefix + 'extension'):
                base_type = XMLWrapper.get_node_attr(child_node, 'base')
                if base_type is not None:
                    base_type = base_type.replace('mstns:', '')
                    if base_type != 'ResponseInfo':
                        response_data.parent_type = base_type

                self._parse_response_xsd_object(xs_prefix, child_node, parent_node, class_name, class_data_map,
                                                response_data)
            elif node_name == (xs_prefix + 'sequence'):
                parent_node_name = XMLWrapper.get_node_name(parent_node)
                if parent_node_name == (xs_prefix + 'complexType'):
                    self._parse_response_xsd_object(xs_prefix, child_node, parent_node, class_name, class_data_map,
                                                    response_data)
            elif node_name == (xs_prefix + 'element'):
                attribute_name = self._get_node_mandatory_attribute(child_node, 'name')
                attribute_type = XMLWrapper.get_node_attr(child_node, 'type')

                if attribute_type is None:
                    inner_type_node = XMLWrapper.get_child_node(child_node, 'complexType', xs_prefix)
                    if inner_type_node is None:
                        raise Exception('API Generator', "Element without type doesn't has 'complexType' node!")

                    inner_node = XMLWrapper.get_child_node(inner_type_node, 'attribute', xs_prefix)
                    if inner_node is not None:
                        if attribute_name.endswith('s'):
                            self._add_attribute_data(response_data, class_name, attribute_name,  attribute_name[:-1],
                                                     'object_list')
                            self._parse_response_xsd_object(xs_prefix, inner_type_node, inner_type_node,
                                                            attribute_name[:-1], class_data_map)
                        else:
                            self._add_attribute_data(response_data, class_name, attribute_name, attribute_name)
                            self._parse_response_xsd_object(xs_prefix, inner_type_node, inner_type_node, attribute_name,
                                                            class_data_map)
                    else:
                        inner_node = XMLWrapper.get_child_node(inner_type_node, 'sequence', xs_prefix)
                        if inner_node is not None:
                            inner_element_node = XMLWrapper.get_child_node(inner_node, 'element', xs_prefix)
                            if inner_element_node is None:
                                raise Exception('API Generator', "Element sequence doesn't has 'element' node!")

                            inner_element_name = self._get_node_mandatory_attribute(inner_element_node, 'name')
                            inner_element_type = XMLWrapper.get_node_attr(inner_element_node, 'type')

                            if inner_element_type is None:
                                inner_element_complex_node = XMLWrapper.get_child_node(inner_element_node,
                                                                                       'complexType',
                                                                                       xs_prefix)
                                if inner_element_complex_node is None:
                                    raise Exception('API Generator', "Element without type doesn't has "
                                                                     "'complexType' node!")

                                self._add_attribute_data(response_data, class_name, attribute_name,
                                                         inner_element_name,
                                                         'object_list')
                                self._parse_response_xsd_object(xs_prefix, inner_element_complex_node,
                                                                inner_element_complex_node, inner_element_name,
                                                                class_data_map)
                            else:
                                inner_element_type = self._get_response_type_name(xs_prefix, inner_element_type)
                                self._add_attribute_data(response_data, class_name, attribute_name,
                                                         inner_element_type,
                                                         'object_list')

                else:
                    attribute_type = self._get_response_type_name(xs_prefix, attribute_type)
                    attribute_type = attribute_type.replace('mstns:', '')

                    max_occurs = XMLWrapper.get_node_attr(child_node, 'maxOccurs')
                    if max_occurs is not None and max_occurs == 'unbounded':
                        self._add_attribute_data(response_data, class_name, attribute_name, attribute_type,
                                                 'object_list')
                    else:
                        self._add_attribute_data(response_data, class_name, attribute_name, attribute_type)

        if class_name not in class_data_map:
            class_data_map[class_name] = response_data

    def _insert_test_method(self, test_api_method_data):
        test_api_data = self.resources['test_cloudshell_api.py'].data

        if self._test_api_position == -1:
            match_result = re.search(self._test_api_flag, test_api_data)
            if match_result is None:
                raise Exception('API Generator', "Can't find begin flag!")

            self._test_api_position = match_result.start()
            test_api_data = test_api_data[:self._test_api_position] + test_api_data[match_result.end() + 1:]

        test_api_data = test_api_data[:self._test_api_position] + test_api_method_data + test_api_data[self._test_api_position:]

        self._test_api_position += len(test_api_method_data)

        self.resources['test_cloudshell_api.py'].data = test_api_data

    def _is_request_node_child_list(self, node):
        first_name = ''
        for child_node in node:
            if len(first_name) == 0:
                first_name = XMLWrapper.get_node_name(child_node)
                continue

            if first_name != XMLWrapper.get_node_name(child_node):
                return False

        return True

    def _parse_request_xml_compex_attr(self, node, node_attr):
        node_name = XMLWrapper.get_node_name(node)
        if XMLWrapper.get_node_child_count(node) == 0:
            node_data = XMLWrapper.get_node_text(node)
            node_attr += "'" + node_data + "', "
        else:
            if self._is_request_node_child_list(node):
                node_attr += "["
                for child_node in node:
                    node_attr += self._parse_request_xml_compex_attr(child_node, "")
                node_attr = node_attr[:-2]
                node_attr += "], "
            else:
                node_attr += "OrderedDict(["
                node_attr += "('__name__', '" + XMLWrapper.get_node_name(node) + "'), "
                for child_node in node:
                    node_attr += "('" + XMLWrapper.get_node_name(child_node) + "', "
                    node_attr += self._parse_request_xml_compex_attr(child_node, "")
                    node_attr = node_attr[:-2]
                    node_attr += "), "
                node_attr = node_attr[:-2]
                node_attr += "]), "

        return node_attr

    def _parse_request_xml_attr(self, node, node_attr):
        node_name = XMLWrapper.get_node_name(node)
        if XMLWrapper.get_node_child_count(node) == 0:
            node_data = XMLWrapper.get_node_text(node)
            node_attr += node_name + "='" + node_data + "', "
        else:
            if self._is_request_node_child_list(node):
                node_attr += node_name + "=["
                for child_node in node:
                    node_attr += self._parse_request_xml_compex_attr(child_node, "")
                node_attr = node_attr[:-2] + "], "
            else:
                node_attr += node_name + "=OrderedDict(["
                node_attr += "('__name__', '" + XMLWrapper.get_node_name(node) + "'), "
                for child_node in node:
                    node_attr += "('" + XMLWrapper.get_node_name(child_node) + "', "
                    node_attr += self._parse_request_xml_compex_attr(node, "")
                    node_attr = node_attr[:-2]
                    node_attr += "), "
                node_attr = node_attr[:-2]

                node_attr = node_attr[:-2] + "]), "
        return node_attr

    def _parse_request_method_attr(self, request_str, classes_data, excluded_params):
        request_node = XMLWrapper.parse_xml(request_str)
        if request_node is None:
            raise Exception('API Generator', "Request XML is empty!")

        node_attr = ""
        for child_node in request_node:
            class_name = XMLWrapper.get_node_name(child_node)
            if class_name in excluded_params:
                continue

            node_attr = self._parse_request_xml_attr(child_node, node_attr)

        if len(node_attr) != 0:
            node_attr = node_attr[:-2]

        return (node_attr)

    def _append_test_method(self, method_name, request_str, test_method_attr):
        test_api_method_data = self.test_api_method_template
        test_api_method_data = test_api_method_data.replace('<method_name>', method_name)

        # this is crutch
        method_name_attr = method_name
        method_name_attr = method_name_attr.replace('CreateImmediateTopologyReservation', 'CreateImmediateReservation')
        method_name_attr = method_name_attr.replace('CreateTopologyReservation', 'CreateReservation')
        test_api_method_data = test_api_method_data.replace('<method_name_attr>', method_name_attr)

        request_str = request_str.replace('\n', '\n' + (' ' * 8))

        test_api_method_data = test_api_method_data.replace('<expect_str>', request_str)
        test_api_method_data = test_api_method_data.replace('<attributes_list>', test_method_attr)

        self._insert_test_method(test_api_method_data)

    def parse_responses(self):
        class_data_map = OrderedDict()

        for child_node in self.api_response_node:
            xs_prefix = XMLWrapper.get_node_prefix(child_node, 'xs')
            if XMLWrapper.get_node_name(child_node) == (xs_prefix + 'complexType'):
                type_name = XMLWrapper.get_node_attr(child_node, 'name')
                if type_name is None:
                    raise Exception('API Generator', 'Wrong response object name!')

                if type_name == 'ApiCommandResult' or type_name == "ResponseInfo":
                    continue

                if type_name in class_data_map:
                    continue

                self._parse_response_xsd_object(xs_prefix, child_node, child_node, type_name, class_data_map)

        for class_name, class_object in class_data_map.items():
            api_response_class = self.api_response_class_template

            # move to serialize method
            attributes = class_object.to_string()
            if len(attributes) != 0:
                attributes = attributes[:-1]
                attributes += '\n'
                attributes +=(' ' * 8) + "CommonResponseInfo.__init__(self, xml_object, find_prefix)"
                if class_object.parent_type != 'CommonResponseInfo':
                    attributes += '\n'
                    attributes += (' ' * 8) + class_object.parent_type + ".__init__(self, xml_object, find_prefix)"
            else:
                if class_object.parent_type == 'CommonResponseInfo':
                    attributes = (' ' * 8) + 'pass'
                else:
                    attributes += (' ' * 8) + class_object.parent_type + ".__init__(self, xml_object, find_prefix)"

            if class_object.parent_type != 'CommonResponseInfo':
                class_name = class_name

            api_response_class = api_response_class.replace('<responcse_name>', class_name)
            api_response_class = api_response_class.replace('<fields>', attributes)
            api_response_class = api_response_class.replace('<parent_type>', class_object.parent_type)
            self._insert_api_response_class(api_response_class)

    def parse_requests(self):
        # iterate trough commands
        for child_node in self.api_node:
            if XMLWrapper.get_node_name(child_node) != 'Command':
                continue

            command_lang = XMLWrapper.get_node_attr(child_node, 'Lang')
            command_lang_list = command_lang.split(';')
            if 'all' not in command_lang_list and 'py' not in command_lang_list:
                continue

            command_name = XMLWrapper.get_node_attr(child_node, 'Name')
            if command_name in ('Introduction', 'UpdateDriver', 'UpdateScript'):
                continue

            decription_node = XMLWrapper.get_child_node(child_node, 'Description')
            command_description = ''
            if decription_node != None:
                command_description = XMLWrapper.get_node_text(decription_node)

            parameters_node = XMLWrapper.get_child_node(child_node, 'Parameters')
            command_params = OrderedDict()

            excluded_params = dict()

            if parameters_node != None:
                for parameter_node in parameters_node:
                    direction_attr = XMLWrapper.get_node_attr(parameter_node, 'Direction')
                    if direction_attr != 'in':
                        continue

                    param_lang = XMLWrapper.get_node_attr(parameter_node, 'Lang')
                    param_lang_list = param_lang.split(';')
                    if 'all' not in param_lang_list and 'py' not in param_lang_list:
                        param_name = XMLWrapper.get_node_attr(parameter_node, 'Name')
                        excluded_params[param_name] = param_name
                        continue

                    param_name = XMLWrapper.get_node_attr(parameter_node, 'Name')
                    if len(param_name) == 0:
                        raise Exception('API Generator', 'Command parameter doesn\'t has "Name" attribute!')

                    param_type = XMLWrapper.get_node_attr(parameter_node, 'Type')
                    if len(param_type) == 0:
                        raise Exception('API Generator', 'Command parameter doesn\'t has "Type" attribute!')

                    param_default_value = XMLWrapper.get_node_attr(parameter_node, 'Default')

                    param_description_node = XMLWrapper.get_child_node(parameter_node, 'Description')
                    param_description = ''
                    if param_description_node is not None:
                        param_description = XMLWrapper.get_node_text(param_description_node)

                    command_params[param_name] = CommandParameterInfo(param_name, param_type.lower(), param_default_value, param_description)

            response_xml = ''
            example_xml_node = XMLWrapper.get_child_node_by_attr(child_node, 'ExampleCode', 'Lang', 'xmlrpc')
            if example_xml_node is not None:
                output_node = XMLWrapper.get_child_node(example_xml_node, 'Output')
                if output_node is not None:
                    response_xml = XMLWrapper.get_node_text(output_node)

            request_node = XMLWrapper.get_child_node_by_attr(child_node, 'Syntax', 'Lang', 'xmlrpc')
            request_xml = ''
            if request_node is not None:
                request_xml = XMLWrapper.get_node_text(request_node)

            self._api_response_class_data[command_name] = (command_params, request_xml)
            self._append_api_method(command_name, command_description, command_params, request_xml)

            # get data for the test
            if self._is_debug:

                classes_data = dict()
                test_method_attr = self._parse_request_method_attr(request_xml, classes_data, excluded_params)

                self._append_test_method(command_name, request_xml, test_method_attr)

    def parse_request_classes(self):
        for key, data_tuple in self._api_response_class_data.items():
            self._append_api_request_class(key, data_tuple[0], data_tuple[1])

    def generate(self):
        #self._read_resources()
        self._read_resources_not_exe()

        self.parse_responses()
        self.parse_requests()

        self.parse_request_classes()

        self._flush_data()
        if len(self._package_name) != 0:
            self._pack_data()

if __name__ == '__main__':
    print 'Run generating...'
    # read args from command line
    key = ''
    arg_data = OrderedDict()
    path_to_exe = ''
    for arg in sys.argv:
        if len(path_to_exe) == 0:
            path_to_exe = arg
        elif len(key) == 0:
            key = arg
        else:
            arg_data[key] = arg
            key = ''

    api_documentation_path = 'APIDocumentation_v6.xml'
    api_response_path = 'ApiCommandResult_v6.xsd'
    if '--input_xml' in arg_data:
        api_documentation_path = arg_data['--input_xml']

    if '--input_xsd' in arg_data:
        api_response_path = arg_data['--input_xsd']

    api_methods_result = 'ApiMethodResults.xml'
    if '--method_result' in arg_data:
        api_methods_result = arg_data['--method_result']

    version = '6.4.0'
    if '--version' in arg_data:
        version = arg_data['--version']

    output_folder = 'genereted_v6'
    if '--output_dir' in arg_data:
        output_folder = arg_data['--output_dir']

    is_debug = '--debug' in arg_data

    package_name = ''
    if '--package_name' in arg_data:
        package_name = arg_data['--package_name']

    package_filename = 'cloudshell-automation-api'
    if '--package_filename' in arg_data:
        package_filename = arg_data['--package_filename']

    package_root_folder = 'cloudshell'
    if '--package_root_dir' in arg_data:
        package_root_folder = arg_data['--package_root_dir']

    api_generator = CloudShellAPIGenerator(api_documentation_path, api_response_path, version,
                                           api_methods_result, output_folder, package_name, package_filename,
                                           package_root_folder, is_debug)
    api_generator.generate()




