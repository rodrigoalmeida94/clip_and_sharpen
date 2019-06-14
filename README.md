# clip_and_sharpen

# Setting up
Dockerfile inspired by @perrygeo https://gist.github.com/perrygeo/1eea522b283baf91dbca497150155695.

Build the image:
```
docker build --tag slimpy:latest .
```
Open `shell` in image:
```
docker run -it --rm slimpy:latest -v /Users/rodrigoalmeida/clip_and_sharpen/tmp:/block/tmp /bin/bash
```
Open `notebook` in image:
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
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
    -t slimpy:latest
```
Replace `/Users/rodrigoalmeida/clip_and_sharpen/tmp/output`and `/Users/rodrigoalmeida/clip_and_sharpen/tmp/input` with location of input and output folder. Place input image (`JP2`, `GeoTiff` or other) in `ìnput` folder.

# Testing
```
docker run \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
    -t slimpy:latest python test.py
```
