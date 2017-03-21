all:
	find . -type f -name '*.png' -delete; \
	find . -type f -name '*.csv' -delete; \
	./bin/go.py -h;

clean:
	find . -type f -name '*.png' -delete; \
	find . -type f -name '*.csv' -delete;

