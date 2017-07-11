# CSCS OpenStack CLI

A complete CLI Docker version can be obtained upon request, but it's relatively easy to make one by hand:

```
$ docker pull ubuntu
$ docker run -it ubuntu
# apt-get update && apt-get install curl wget vim python-pip less python-pysaml2 libssl-dev iputils-ping git
# pip install -U pip setuptools
# pip install -U python-openstackclient lxml oauthlib
```

In order to load the environment, download and source the [pollux.env](pollux.env) file above. 
```
# cd /root
# git clone https://github.com/eth-cscs/openstack
# cd openstack/cli/
```
It should output something like this:
```
# source pollux.env
 * Creating environment for openstack CLI:
Username: myusername
Password: 
 * Got an unscoped token, preparing environment...
1) 1237688701212123ab221e5cf9d59111 project1
2) 12401230ebcd1121241234148306065a project2
Please choose an option: 2
 * Selected project project2: 12401230ebcd1121241234148306065a
 * Environment ready for openstack CLI with scoped project: project2
```

You can also use a parameter ```source pollux.env my_proj``` with the name of your project (or part of it) in order to avoid the menu from popping up, if that's what you want.
