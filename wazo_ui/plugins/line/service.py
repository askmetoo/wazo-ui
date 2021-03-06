# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from wazo_ui.helpers.service import BaseConfdService


class LineService(BaseConfdService):

    resource_confd = 'lines'

    def __init__(self, confd_client):
        self._confd = confd_client

    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    def get_context(self, context):
        result = self._confd.contexts.list(name=context)
        for context in result['items']:
            return context

    def get_endpoint_sip(self, endpoint_id):
        return self._confd.endpoints_sip.get(endpoint_id)

    def get_endpoint_custom(self, endpoint_id):
        return self._confd.endpoints_custom.get(endpoint_id)

    def create(self, resource):
        resource_created = super().create(resource)
        resource['id'] = resource_created['id']
        if resource.get('endpoint_sip'):
            endpoint_sip = self._confd.endpoints_sip.create(resource['endpoint_sip'])
            self._confd.lines(resource['id']).add_endpoint_sip(endpoint_sip['id'])
        if resource.get('endpoint_custom'):
            endpoint_custom = self._confd.endpoints_custom.create(resource['endpoint_custom'])
            self._confd.lines(resource['id']).add_endpoint_custom(endpoint_custom['id'])

    def update(self, resource):
        super().update(resource)
        if resource.get('endpoint_sip'):
            self._confd.endpoints_sip.update(resource['endpoint_sip'])
        if resource.get('endpoint_custom'):
            self._confd.endpoints_custom.update(resource['endpoint_custom'])
