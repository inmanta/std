FROM rockylinux:8
ENV container docker

ARG PIP_INDEX_URL
ARG PIP_PRE

RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]

RUN yum install -y python3 glibc-locale-source

RUN localedef -i en_US -f UTF-8 en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

RUN mkdir -p /module/std
WORKDIR /module/std

RUN python3 -m venv env
RUN env/bin/pip install -U pip

COPY requirements.txt requirements.txt
COPY requirements.freeze requirements.freeze
COPY requirements.dev.txt requirements.dev.txt

RUN env/bin/pip install --only-binary asyncpg -r requirements.txt -r requirements.dev.txt -c requirements.freeze

COPY module.yml module.yml
COPY model model
COPY plugins plugins
COPY tests tests

CMD ["/usr/sbin/init"]
