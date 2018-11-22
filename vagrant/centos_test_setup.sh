#!/bin/bash
set -x

sudo -u centos -- ssh-keygen -q -t rsa -N '' -f /home/centos/.ssh/id_rsa
cat /home/centos/.ssh/id_rsa.pub >>/root/.ssh/authorized_keys 