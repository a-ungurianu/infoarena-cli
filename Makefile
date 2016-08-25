.PHONEY: scrap

# This just runs whatever I have in the scrapbook.py file, which I use to
# test stuff
scrap:
	cd tests && \
	python3 scrapbook.py
