ARG PYTHON_VERSION=3.9
ARG PIP_INDEX_URL
ARG PIP_PRE

FROM python:$PYTHON_VERSION

ENV container docker

ARG PYTHON_VERSION=39
ARG PIP_INDEX_URL
ARG PIP_PRE


WORKDIR /module/std

# Copy the entire module into the container
COPY . .

RUN rm -rf env && python3 -m venv env && env/bin/pip install -U pip
# The module set tests convert the module into a V2 module, install it in the test
# environment and run the tests against it. This code ensures that the module is
# installed as a V2 module when it contains a inmanta_plugins directory.
#RUN #if [ -e "inmanta_plugins" ]; then \
#    env/bin/pip install --only-binary asyncpg -r requirements.dev.txt -c requirements.freeze; \
#    rm -rf ./dist; \
#    env/bin/inmanta module build; \
#    env/bin/pip install -c requirements.freeze ./dist/*.whl; \
#else \
#    env/bin/pip install --only-binary asyncpg -r requirements.txt -r requirements.dev.txt -c requirements.freeze; \
#fi

RUN env/bin/pip install --only-binary asyncpg -r requirements.txt -r requirements.dev.txt -c requirements.freeze;

#CMD [ "env/bin/python", "-m", "env/bin/pytest", "tests/", "-v", "--junitxml=junit.xml"]
CMD [ "env/bin/python", "-m", "pytest", "tests/", "-vv", "--junitxml=junit.xml"]
#CMD [ "python", "--version"]



#CMD [ "env/bin/pip", "list"]
