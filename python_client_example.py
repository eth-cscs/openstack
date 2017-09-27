#!/usr/bin/env python
#
# This is a sample program on how to use the OpenStack python bindings at CSCS
#
#    Copyright (C) 2017, ETH Zuerich, Switzerland
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    AUTHOR  Pablo Fernandez 
#    DATE    September 27th, 2017

# WARNING: this program requires the openstack python libraries installed. Please refer to https://github.com/eth-cscs/openstack/tree/master/cli for instructions.

from keystoneauth1.identity import v3
from keystoneauth1 import session
import getpass, os
from keystoneauth1.extras._saml2 import V3Saml2Password
OS_AUTH_URL = os.environ['OS_AUTH_URL'] if 'OS_AUTH_URL' in os.environ else 'https://pollux.cscs.ch:13000/v3'
OS_IDENTITY_PROVIDER = os.environ['OS_IDENTITY_PROVIDER'] if 'OS_IDENTITY_PROVIDER' in os.environ else 'cscskc'
OS_IDENTITY_PROVIDER_URL = os.environ['OS_IDENTITY_PROVIDER_URL'] if 'OS_IDENTITY_PROVIDER_URL' in os.environ else 'https://kc.cscs.ch/auth/realms/cscs/protocol/saml/'
OS_PROTOCOL = os.environ['OS_PROTOCOL'] if 'OS_PROTOCOL' in os.environ else 'mapped'

### Authenticate user:
user = getpass.getpass("Username: ")
pw = getpass.getpass()
auth = V3Saml2Password(auth_url=OS_AUTH_URL, identity_provider=OS_IDENTITY_PROVIDER, protocol=OS_PROTOCOL, identity_provider_url=OS_IDENTITY_PROVIDER_URL, username=user, password=pw)
sess = session.Session(auth=auth)
print "User info:", user, sess.get_user_id()

### To list user's projects:
from keystoneclient.v3 import client
ks = client.Client(session=sess, interface='public')
projects = ks.projects.list(user=sess.get_user_id())
print "Projects:", [t.name for t in projects]
print "Project[0]:", projects[0]

### To list project's Swift containers (needs an scoped token):
import swiftclient.client as swiftclient
auth2 = v3.Token(auth_url=OS_AUTH_URL, token=sess.get_token(), project_id=projects[0].id)
sess2 = session.Session(auth=auth2)
conn2 = swiftclient.Connection(session=sess2)
resp_headers, containers = conn2.get_account()
print "Containers:", [container['name'] for container in containers]
