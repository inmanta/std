#!/bin/bash
set -x

sudo -u centos -- ssh-keygen -q -t rsa -N '' -f /home/centos/.ssh/id_rsa
cat /home/centos/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys 

sudo -u centos python3 -m venv /home/centos/venv

sudo -u centos /home/centos/venv/bin/python3 -m pip install --upgrade pip
sudo -u centos /home/centos/venv/bin/python3 -m pip install inmanta pytest-inmanta 