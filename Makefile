all:
	find . -type f -name '*.png' -delete; \
	find . -type f -name '*.csv' -delete; \
	find . -type f -name 'AST.txt' -delete; \
	./bin/go.py -h;

clean:
	find . -type f -name '*.png' -delete; \
	find . -type f -name '*.csv' -delete; \
	find . -type f -name 'AST.txt' -delete;
