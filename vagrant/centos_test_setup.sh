#!/bin/bash
set -x

sudo -u jenkins -- ssh-keygen -q -t rsa -N '' -f /home/centos/.ssh/id_rsa
cat /home/centos/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys 

python3 -m venv /opt/venv

/opt/venv/bin/python3 -m pip install --upgrade pip
/opt/venv/bin/python3 -m pip install inmanta pytest-inmanta 