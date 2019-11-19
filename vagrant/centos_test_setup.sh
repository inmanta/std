#!/bin/bash
set -x

sudo -u centos -- ssh-keygen -q -t rsa -N '' -f /home/centos/.ssh/id_rsa
cat /home/centos/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys

sudo -u centos -- /home/centos/venv/bin/python3 -m pip install --upgrade pip
sudo -u centos -- /home/centos/venv/bin/python3 -m pip install -c https://raw.githubusercontent.com/inmanta/inmanta/master/requirements.txt inmanta
sudo -u centos -- /home/centos/venv/bin/python3 -m pip install -r https://raw.githubusercontent.com/inmanta/std/${BRANCH_NAME}/requirements.txt
sudo -u centos -- /home/centos/venv/bin/python3 -m pip install -r https://raw.githubusercontent.com/inmanta/std/${BRANCH_NAME}/requirements.dev.txt
