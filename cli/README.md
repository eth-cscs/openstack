# CSCS OpenStack CLI

Having the Openstack CLI working is relatively easy. You can choose between:

## Option A
Creating a Docker container and installing everything inside
```
$ docker pull ubuntu
$ docker run -it ubuntu
# apt-get update && apt-get install curl wget vim python-pip less python-pysaml2 libssl-dev iputils-ping git
# pip install -U pip setuptools
# pip install -U python-openstackclient lxml oauthlib python-swiftclient
```

Then in order to load the environment, download and source the [pollux.env](pollux.env) file above. 
```
# cd /root
# git clone https://github.com/eth-cscs/openstack
# source openstack/cli/pollux.env
```
Now don't forget to commit your Docker image, from another shell, so that these changes are not lost: ```docker commit 123someid123 openstack_cli``` (you can get the ID with ```docker ps```). Otherwise you need to start from scratch next time you do a ```docker run```

## Option B
Alternatively, you can also do this with python virtual environments:
```
$ virtualenv openstack_cli
$ source openstack_cli/bin/activate
$ pip install -U pip setuptools
$ pip install -U python-openstackclient lxml oauthlib python-swiftclient
# If you have problems, maybe your distribution is missing some packages. Please check the apt-get command above.

```
And then load the Pollux environment files:
```
$ cd openstack_cli
$ git clone https://github.com/eth-cscs/openstack
$ source openstack/cli/pollux.env
```

## Output should look like this
```
$ source pollux.env
 * Creating environment for openstack CLI:
Username: myusername
Password: 
[openstack --os-auth-type v3samlpassword token issue]
 * Got an unscoped token, preparing environment...
[openstack project list]
1) 1237688701212123ab221e5cf9d59111 project1
2) 12401230ebcd1121241234148306065a project2
Please choose an option: 2
 * Selected project project2: 12401230ebcd1121241234148306065a
[openstack --os-project-id 12401230ebcd1121241234148306065a token issue]
 * Environment ready for openstack CLI with scoped project: project2
```

You can also use a parameter ```source pollux.env my_proj``` with the name of your project (or part of it) in order to avoid the menu from popping up, if that's what you want. It works like a grep.
