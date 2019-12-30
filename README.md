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
