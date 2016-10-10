# Redis Work

The goal of this project is to showcase how to:

* Showcase how to test that a redis cluster is working.
* Trigger failures, and illustrate operational functionality afterwards.
* Leave the cluster in a happy state.
* Provide a template for future testing ( RabbitMQ, MongoDB, etc).

## Getting Started:

Tools Used:

* Python 2.7
* VirtualEnv
* Fabric
* Python Redis Library ( redis ) 
* Docker
* Docker UCP & DTR
* Git
* PyMongo ( MongoDB Python Library )
* Pika ( Python RabbitMQ Library)

The links below will cover the basics of the libraries used in this test suite.

### Testing Project Setup:

First you will need to clone this project locally to get started with testing:

```
git clone (some address here) rediswork
```

Next CD into the project to get started.

```
cd rediswork
```

### VirtualEnv: 

This is a solution that allows for the creation of isolated Python environments where 3rd party dependencies can be installed and leveraged without polluting the system as a whole. To install it on Ubuntu follow the instructions below:

```
sudo apt-get update
sudo apt-get dist-upgrade
sudo reboot
```
Reconnect.

Configure Python & Build Tools

```
sudo apt-get install python-pip python-dev build-essential
sudo apt-get install git-core
sudo pip install --upgrade virtualenv
sudo pip install virtualenvwrapper
```

Now Configure Virtualenv & Virtualenv Wrapper

edit "~/.bashrc" by appending:

```
# Python Info
export WORKON_HOME=~/.virtualenvs
. /usr/local/bin/virtualenvwrapper.sh
```

Now reload your session with:

```
source ~/.bashrc
```

Before continuing you will need to create a virtualenv for this testing:

```
mkvirtualenv rediswork
```

To install all of the dependencies:

```
pip install -r requirements.txt
```

At this point you will have all the code required to execute the tests. If you end your shell session execute the 2 commands below to resume your testing.

```
workon rediswork
cd /path/to/rediswork
```

### How to Execute the Tests:

Open A Session:

```
workon rediswork
cd /path/to/rediswork
``` 

Next deploy Redis using the attached docker-compose.yml file, once done identify the 3 nodes running HA proxy and update the test_redis_driver.py file to have the correct IPs of the swarm nodes.

If you would like to avoid passwords during testing, add your local users ssh public key to the root user on each node.

To learn more about that: https://linuxconfig.org/passwordless-ssh

Finally to actually invoke the tests:

```
python test_redis_driver.py
```

### Fabric

Fabric is a 3rd party library for automating the execution of local and shell commands. To learn more: http://www.fabfile.org/

### Python Redis Module

The Redis package allows for Python scripts and software to fully control an existing Redis installation. To learn more: https://pypi.python.org/pypi/redis

### Pika

Pika is the official library for connecting and utilizing RabbitMQ reasources in Python. To learn more: http://pika.readthedocs.io/en/0.10.0/intro.html

### Questions and comments

If you have any issues with the above code, please contact Chris King at chris.king@kilncode.com and I'll respond as quickly as possible.

