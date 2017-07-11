#!/bin/bash

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
#    DATE    July 8th, 2017

echo "Listing existing containers"
openstack container list
if [ $? -ne 0 ]; then
    echo Failed to list containers... you are probably not authorized
    exit
fi

NAME=swift-test-$RANDOM
echo "Creating container $NAME"
openstack container create $NAME

echo "Creating file inside container"
echo "swift_test" > /tmp/$NAME
openstack object create $NAME /tmp/$NAME

echo "Displaying object information"
openstack object show $NAME /tmp/$NAME

echo "Downloading object"
mv /tmp/$NAME /tmp/2_$NAME
openstack object save $NAME /tmp/$NAME 
diff /tmp/$NAME /tmp/2_$NAME
if [ $? -ne 0 ]; then
    echo "ERROR: Files are different!"
else
    echo "SUCCESS: Files match!"
fi

echo "Cleaning up..."
openstack object delete $NAME /tmp/$NAME
openstack container delete $NAME
rm /tmp/$NAME /tmp/2_$NAME

