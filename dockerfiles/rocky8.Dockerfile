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

# Copy the entire module into the container
COPY . .

RUN rm -rf env && python3 -m venv env && env/bin/pip install -U pip
# The module set tests convert the module into a V2 module, install it in the test
# environment and run the tests against it. This code ensures that the module is
# installed as a V2 module when it contains a inmanta_plugins directory.
RUN if [ -e "inmanta_plugins" ]; then \
    env/bin/pip install --only-binary asyncpg -r requirements.dev.txt -c requirements.freeze; \
    env/bin/inmanta module install .; \
else \
    env/bin/pip install --only-binary asyncpg -r requirements.txt -r requirements.dev.txt -c requirements.freeze; \
fi

CMD ["/usr/sbin/init"]
