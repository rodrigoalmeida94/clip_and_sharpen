# clip_and_sharpen

# Setting up
## Docker
Dockerfile by @perrygeo https://gist.github.com/perrygeo/1eea522b283baf91dbca497150155695.

Build the image:
```
docker build --tag slimpy:latest .
```
Open shell in image:
```
docker run -it --rm slimpy:latest /bin/bash
```
Open notebook in image:
```
docker run -it --rm \
		-p 0.0.0.0:8888:8888 \
		--rm \
		--interactive \
		--tty \
		--volume $(shell pwd)/notebooks/:/notebooks \
		slimpy:latest  /bin/bash -c "cd /notebooks && jupyter notebook --ip=0.0.0.0 --allow-root"
```

# Running
```
docker run \
    -e UP42_TASK_PARAMETERS="$(cat params.json)" \
    -v /tmp/output:/tmp/output \
    -t data-block
```
