SHELL := /bin/zsh

p: prepair
prepair:
	npm i -g nodemon

f: freeze
freeze:
	pip freeze > requirements.txt

i: install
install:
	pip install -r requirements.txt

r: run
run:
	python src/main.py download

r.s:
	python src/main.py download --skipDownload

m: mergePDF
mergePDF:
	python src/main.py mergePDF

d: dev
dev:
	# nodemon --exec python src/main.py mergePDF
	nodemon --exec python src/main.py makePDFs

m:
	python src/main.py makePDFs

# clean pdfs
clean:
	for dir in ./pdfs/*(/) ./pdfs/*/*(/) ./pdfs/*/*/*(/); do \
		if [[ -z $$(ls -A $$dir) ]]; then \
			rmdir $$dir; \
		fi; \
	done
