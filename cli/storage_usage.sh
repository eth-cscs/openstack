#!/bin/bash

# This script prints the block storage and object storage usage of all projects a user belongs to

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
#    AUTHORS Marco Passerini & Pablo Fernandez & Massimo Benini
#    DATE    July 17th, 2019

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && \
  echo "USAGE INFO: you need source this script (source $0 or . $0)." && \
  echo "  You can also pass a parameter that serves a project name filter (for scoped tokens)" && exit

read -p 'Username: ' uservar
read -sp 'Password: ' passvar
echo ""

# Prepare environment
for key in $( set | awk '{FS="="}  /^OS_/ {print $1}' ); do unset $key ; done
export OS_USERNAME=$uservar
export OS_PASSWORD=$passvar
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_URL=https://pollux.cscs.ch:13000/v3
export OS_IDENTITY_PROVIDER=cscskc
export OS_IDENTITY_PROVIDER_URL=https://auth.cscs.ch/auth/realms/cscs/protocol/saml/
export OS_PROTOCOL=mapped
export OS_INTERFACE=public

#Getting the unscoped token:
UNSCOPED_TOKEN="$(openstack --os-auth-type v3samlpassword token issue --format value --column id)"
# Remove the password from the environment, for security

if [ $? -ne 0 ]; then
    echo " * Failed to get unscoped token, exit"
    unset OS_PASSWORD 
    return
fi

export OS_AUTH_TYPE=token
export OS_TOKEN=$UNSCOPED_TOKEN
unset OS_PASSWORD

# Getting the user ID with python directly (no other way, plus serves as an example!!)
python <<EOF
from keystoneauth1.identity import v3
from keystoneauth1 import session
auth = v3.Token(auth_url="$OS_AUTH_URL", token="$OS_TOKEN")
sess = session.Session(auth=auth)
print(sess.get_user_id())
EOF

PROJECTS="$(openstack project list -f csv --quote minimal|awk '{if(NR>1)print}')"

for PROJECT in $PROJECTS
do
  PROJECT_NAME=$(echo $PROJECT|cut -f 2 -d ',')
  PROJECT_ID=$(echo $PROJECT|cut -f 1 -d ',')
  echo "### $PROJECT_NAME ###"
  #Getting the scoped token:
  SCOPED_TOKEN="$(openstack --os-project-id $PROJECT_ID token issue --format value --column id)"
  if [ $? -ne 0 ]; then
      echo " * WARNING: Failed to get scoped token, but unscoped commands should work fine"
      return
  fi
  export OS_TOKEN=$SCOPED_TOKEN
  export OS_PROJECT_ID=$PROJECT_ID
  alias swift='swift --os-auth-token $OS_TOKEN --os-storage-url https://object.cscs.ch/v1/AUTH_$OS_PROJECT_ID'
  BLOCK_USED=$(openstack volume list -f value -c Size | paste -sd+ | bc)
  BLOCK_USED=${BLOCK_USED:-0}
  BLOCK_LIMIT=$(openstack quota show -f shell | grep '^gigabytes="' | sed 's/^gigabytes="\([0-9]*\)"/\1/')
  BLOCK_LIMIT=${BLOCK_LIMIT:-0}
  OBJ_USED_POLICY0=$(swift stat | grep 'Bytes in policy "policy-0":' | awk '{ print $5 }')
  OBJ_USED_POLICY0=${OBJ_USED_POLICY0:-0}
  OBJ_USED_VERSIONS=$(swift stat | grep 'Bytes in policy "versions":' | awk '{ print $5 }')
  OBJ_USED_VERSIONS=${OBJ_USED_VERSIONS:-0}
  OBJ_USED=$(($OBJ_USED_POLICY0 + $OBJ_USED_VERSIONS))
  OBJ_LIMIT=$(swift stat | grep 'Meta Quota-Bytes:' |  awk '{ print $3 }')
  OBJ_LIMIT=${OBJ_LIMIT:-0}
  echo "Block storage used GB:"
  echo $BLOCK_USED
  echo "Block storage limit GB:"
  echo $BLOCK_LIMIT
  echo "Object storage used bytes:"
  echo $OBJ_USED
  echo "Object storage limit bytes:"
  echo $OBJ_LIMIT
done

