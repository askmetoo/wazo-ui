# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from flask import session, url_for
from flask_login.mixins import UserMixin


class UserUI(UserMixin):

    def __init__(self, token, uuid=None):
        self._token = token
        self.uuid = uuid
        if 'instance' not in session:
            session['instance'] = None

    def get_id(self):
        return self._token

    def get_user(self):
        return session.get('user')

    def get_tenant(self):
        return session.get('user_tenant')

    def get_displayname(self):
        return session['user']['username']

    def get_tenant_uuid(self):
        if 'working_tenant_uuid' in session:
            return session['working_tenant_uuid']

        return session['user'].get('tenant_uuid')

    def get_user_index_url(self):
        return url_for('wazo_engine.user.UserView:index')

    def get_current_instance_tenants(self):
        instance = self.get_instance()
        if not instance:
            return []

        return session['instance_tenants'] if 'instance_tenants' in session else []

    def reset_instance(self):
        session['instance'] = None
        session['instance_tenants'] = []

    def set_tenant(self, tenant=None):
        session['instance'] = {}
        session['instance'] = {'remote_host': 'localhost'}
        session['instance']['wazo_tenant'] = tenant

    def get_instance(self):
        return session['instance']

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
