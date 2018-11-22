#!/bin/bash
set -x

yum install -y epel-release
yum update -y
yum install -y git python34 python34-setuptools python34-pip python34-devel

ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys 

python3 -m venv /opt/venv

/opt/venv/bin/python3 -m pip install --upgrade pip
/opt/venv/bin/python3 -m pip install inmanta pytest-inmanta 