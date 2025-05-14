#!/usr/bin/env python

import os

from setuptools import setup

setup(name='oab-vsphere-automation-sdk',
      version='1.86.0',
      description='VMware vSphere Automation SDK for Python',
      url='https://github.com/vmware/vsphere-automation-sdk-python',
      author='VMware, Inc.',
      license='MIT',
      packages=[],
      install_requires=[
        'lxml >= 4.3.0',
        'pyVmomi >=6.7',
        'oab-vapi-runtime==2.44.0',
        'oab-vcenter-bindings==4.2.0',
        'oab-vapi-common-client==2.44.0',
        'oab-vmwarecloud-aws==1.64.0',
        'oab-nsx-python-sdk==4.1.2.0.0',
        'oab-nsx-policy-python-sdk==4.1.2.0.0',
        'oab-nsx-vmc-policy-python-sdk==4.1.2.0.0',
        'oab-nsx-vmc-aws-integration-python-sdk==4.1.2.0.0',
        'oab-vmwarecloud-draas==1.23.0',
      ]
)
