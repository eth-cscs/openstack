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
OS_IDENTITY_PROVIDER_URL = os.environ['OS_IDENTITY_PROVIDER_URL'] if 'OS_IDENTITY_PROVIDER_URL' in os.environ else 'https://auth.cscs.ch/auth/realms/cscs/protocol/saml/'
OS_PROTOCOL = os.environ['OS_PROTOCOL'] if 'OS_PROTOCOL' in os.environ else 'mapped'
OS_INTERFACE = os.environ['OS_INTERFACE'] if 'OS_INTERFACE' in os.environ else 'public'

if 'OS_TOKEN' in os.environ:
  # We've already been authenticated. We can just set the right variables
  OS_TOKEN = os.environ['OS_TOKEN']
  OS_USERNAME = os.environ['OS_USERNAME']
  auth = v3.Token(auth_url=OS_AUTH_URL, token=OS_TOKEN)
else: 
  ### Authenticate user:
  OS_USERNAME = getpass.getpass("Username: ")
  pw = getpass.getpass()
  auth = V3Saml2Password(auth_url=OS_AUTH_URL, identity_provider=OS_IDENTITY_PROVIDER, protocol=OS_PROTOCOL, identity_provider_url=OS_IDENTITY_PROVIDER_URL, username=OS_USERNAME, password=pw)

sess = session.Session(auth=auth)
print "User info:", OS_USERNAME, sess.get_user_id()

if 'OS_PROJECT_ID' in os.environ:
  # The token we've got from the environment is already scoped
  OS_PROJECT_ID = os.environ['OS_PROJECT_ID']
else:
  ### List user's projects:
  from keystoneclient.v3 import client
  ks = client.Client(session=sess, interface=OS_INTERFACE)
  projects = ks.projects.list(user=sess.get_user_id())
  print "Available projects:", [t.name for t in projects]
  OS_PROJECT_ID = projects[0].id

print "Selected project: ", OS_PROJECT_ID
# (Re-)Scope the session
auth = v3.Token(auth_url=OS_AUTH_URL, token=sess.get_token(), project_id=OS_PROJECT_ID)
sess = session.Session(auth=auth)

### To list project's Swift containers (needs an scoped token, or re-scope the previous one):
import swiftclient.client as swiftclient
conn = swiftclient.Connection(session=sess)
resp_headers, containers = conn.get_account()
print "Containers:", [container['name'] for container in containers]
