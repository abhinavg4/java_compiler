all:
	find . -type f -name '*.png' -delete; \
	./bin/go.py -h;

clean:
	find . -type f -name '*.png' -delete;
