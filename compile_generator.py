__author__ = 'g8y3e'

from distutils.core import setup
import py2exe, sys, os

API_DATA_V6 = open('template/python/api/cloudshell_api_v6.py').read()
API_DATA_V7 = open('template/python/api/cloudshell_api_v7.py').read()
COMMON_API_DATA = open('template/python/api/common_cloudshell_api.py').read()
API_TEST_DATA = open('template/python/api/test_cloudshell_api.py').read()

API_METHOD_TEMPLATE = open('template/python/api/api_method_template').read()
API_RESPONSE_OBJ = open('template/python/api/api_response_object_template').read()
TEST_API_METHOD_TEMPLATE = open('template/python/api/test_api_method_template').read()

setup(name="CloudShellAPIGenerator",
      version="1.0",
      description="Generate API for CloudShell",
      author="g8y3e",
      options={'py2exe': {
          'bundle_files': 1,
          'compressed': True,
          'includes': ['lxml.etree', 'lxml._elementpath', 'gzip']
      }},
      console=[{'script': 'api_generator.py',
                'icon_resources': [(0, 'img/icon.ico')],
                'other_resources': [(u'COMMON_API', 1, COMMON_API_DATA),
                                    (u'API_V6', 1, API_DATA_V6),
                                    (u'API_V7', 1, API_DATA_V7),
                                    (u'API_TEST', 1, API_TEST_DATA),

                                    (u'API_METHOD_TMP', 1, API_METHOD_TEMPLATE),
                                    (u'API_RESPONSE_TMP', 1, API_RESPONSE_OBJ),
                                    (u'TEST_API_METHOD_TMP', 1, TEST_API_METHOD_TEMPLATE)]}])