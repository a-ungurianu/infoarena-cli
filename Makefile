.PHONEY: scrap

scrap:
	cd tests && \
	python3 scrapbook.py
