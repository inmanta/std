# STD

The inmanta standard library.

## How to run the tests in docker

Some of the tests run against systemd, which testing against on developers own systems would not be ideal.
Instead this module has a docker file to run the tests in, so that they are nice and isolated:

```bash
docker build . -t test-module-std
docker run -d --rm --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name std-tests test-module-std
docker exec std-tests env/bin/pytest tests -v
```

Stopping the container (`docker stop std-tests`) will also clean up the volumes.

## Using pytest to set up the container

It is also possible to set up the container and run the tests in it via pytest.
This is controlled by the `INMANTA_TEST_INFRA_SETUP` environment variable.
When it's set to `true`, the container is started, and torn down automatically after the tests.
In this case, the test driver (which is the test case in `test_in_docker.py`) is the only one executed outside the container,
while the rest of the test cases are executed inside the container.
The test results can be found in the `junit_docker.xml` file (outside the container).

The cleanup behavior can be changed by the `INMANTA_NO_CLEAN` environment variable,
when set to `true`, the container is not stopped after the tests.
