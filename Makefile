.PHONEY: test

test:
	cd tests && \
	python3 scrapbook.py
