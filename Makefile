all:
	[ -e *.png ] && rm *.png; \
	./bin/go.py -h;

clean:
	rm *.png;
