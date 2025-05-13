# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Copyright 2023 VMware, Inc.  All rights reserved.

# AUTO GENERATED FILE -- DO NOT MODIFY!
#
# vAPI stub file for package com.vmware.vcenter.lcm.deployment.common.
#---------------------------------------------------------------------------

"""
The ``com.vmware.vcenter.deployment.common`` module provides common classes for
install/upgrade of a vCenter Server.

"""

__author__ = 'VMware, Inc.'
__docformat__ = 'restructuredtext en'

import sys
from warnings import warn

from vmware.vapi.bindings import type
from vmware.vapi.bindings.converter import TypeConverter
from vmware.vapi.bindings.enum import Enum
from vmware.vapi.bindings.error import VapiError
from vmware.vapi.bindings.struct import VapiStruct
from vmware.vapi.bindings.stub import (
    ApiInterfaceStub, StubFactoryBase, VapiInterface)
from vmware.vapi.bindings.common import raise_core_exception
from vmware.vapi.data.validator import (UnionValidator, HasFieldsOfValidator)
from vmware.vapi.exception import CoreException
from vmware.vapi.lib.constants import TaskType
from vmware.vapi.lib.rest import OperationRestMetadata

class AllocateResource(Enum):
    """
    The ``AllocateResource`` class defines when to allocate resource to VM.
    This enumeration was added in vSphere API 8.0.2.0.

    .. note::
        This class represents an enumerated type in the interface language
        definition. The class contains class attributes which represent the
        values in the current version of the enumerated type. Newer versions of
        the enumerated type may contain new values. To use new values of the
        enumerated type in communication with a server that supports the newer
        version of the API, you instantiate this class. See :ref:`enumerated
        type description page <enumeration_description>`.
    """
    ON_DEPLOYMENT = None
    """
    On deployment of the VM allocate the resource to the target VM. This class
    attribute was added in vSphere API 8.0.2.0.

    """
    ON_SUCCESSFUL_UPGRADE = None
    """
    On successful upgrade of the VC allocate the resource to the target VM.
    This class attribute was added in vSphere API 8.0.2.0.

    """

    def __init__(self, string):
        """
        :type  string: :class:`str`
        :param string: String value for the :class:`AllocateResource` instance.
        """
        Enum.__init__(string)

AllocateResource._set_values({
    'ON_DEPLOYMENT': AllocateResource('ON_DEPLOYMENT'),
    'ON_SUCCESSFUL_UPGRADE': AllocateResource('ON_SUCCESSFUL_UPGRADE'),
})
AllocateResource._set_binding_type(type.EnumType(
    'com.vmware.vcenter.lcm.deployment.common.allocate_resource',
    AllocateResource))




class ResourceAllocationInfo(VapiStruct):
    """
    The ``ResourceAllocationInfo`` class contains resource allocation
    information of VM. This class was added in vSphere API 8.0.2.0.

    .. tip::
        The arguments are used to initialize data attributes with the same
        names.
    """




    def __init__(self,
                 reservation=None,
                 allocate=None,
                ):
        """
        :type  reservation: :class:`long`
        :param reservation: Amount of resource that is guaranteed available to the virtual
            machine. Reserved resources are not wasted if they are not used. If
            the utilization is less than the reservation, the resources can be
            utilized by other running virtual machines. Units are MB for
            memory, and MHz for CPU. This attribute was added in vSphere API
            8.0.2.0.
        :type  allocate: :class:`AllocateResource` or ``None``
        :param allocate: This attribute was added in vSphere API 8.0.2.0.
            If None will allocate resource at VM deployment.
        """
        self.reservation = reservation
        self.allocate = allocate
        VapiStruct.__init__(self)


ResourceAllocationInfo._set_binding_type(type.StructType(
    'com.vmware.vcenter.lcm.deployment.common.resource_allocation_info', {
        'reservation': type.IntegerType(),
        'allocate': type.OptionalType(type.ReferenceType(__name__, 'AllocateResource')),
    },
    ResourceAllocationInfo,
    False,
    None))




class StubFactory(StubFactoryBase):
    _attrs = {
    }

