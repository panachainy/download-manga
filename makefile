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
download: run
run:
	python src/main.py download

merge: mergePDF
mergePDF:
	python src/main.py mergePDFs

d: dev
dev:
	# nodemon --exec python src/main.py mergePDFs
	nodemon --exec python src/main.py makePDFs

make:
	python src/main.py makePDFs

# clean pdfs
clean:
	for dir in ./pdfs/*(/) ./pdfs/*/*(/) ./pdfs/*/*/*(/); do \
		if [[ -z $$(ls -A $$dir) ]]; then \
			rmdir $$dir; \
		fi; \
	done
