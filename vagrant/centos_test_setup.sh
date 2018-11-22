#!/bin/bash
set -x

sudo yum install -y epel-release
sudo yum update -y
sudo yum install -y git python34 python34-setuptools python34-pip python34-devel

ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa
sudo cat ~/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys 

python3 -m venv ~/venv

~/venv/bin/python3 -m pip install --upgrade pip
~/venv/bin/python3 -m pip install inmanta pytest-inmanta 