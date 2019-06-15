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
		--volume /Users/rodrigoalmeida/clip_and_sharpen/notebooks/:/notebooks \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
		slimpy:latest  /bin/bash \
		-c "cd /notebooks && jupyter notebook --ip=0.0.0.0 --allow-root"
```

# Running
Replace `/Users/rodrigoalmeida/clip_and_sharpen/tmp/output`and `/Users/rodrigoalmeida/clip_and_sharpen/tmp/input` with location of input and output folder.
*Place input image (`JP2`, `GeoTiff` or other) in `ìnput` folder, this should be the only file in folder.*
```
docker run \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
    -t slimpy:latest
```

## Run with additional parameters
```
docker run \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
		-t slimpy:latest \
		python run.py --clip-coords 2000 2000 250 250
```
Where `--clip-coords`is `(column_offset, row_offset, width, height)`.

```
docker run \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
		-t slimpy:latest \
		python run.py --clip-coords 2000 2000 250 250 --alpha 10
```
Where `--alpha`is parameter for edge salience in sharpen method.

```
docker run \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
		-v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
		-t slimpy:latest \
		python run.py --filter-type 3x3
```
Where `--filter-type`is either `gaussian`or `3x3`.

# Visualization
Check out this [notebook](notebooks/visualization.ipynb).

# Testing
```
docker run \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/output:/tmp/output \
    -v /Users/rodrigoalmeida/clip_and_sharpen/tmp/input:/tmp/input \
    -t slimpy:latest \
		python test.py -v
```
