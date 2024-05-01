SHELL := /bin/zsh

p: prepair
prepair:
	npm i -g nodemon

sh:
	poetry shell

r: run
download: run
run:
	python src/main.py download

load_config:
	python src/main.py load_config

load_download:
	go run main.go

make:
	python src/main.py makePDFs

merge: mergePDF
mergePDF:
	python src/main.py mergePDFs

pdf:
	python src/main.py makePDFs
	python src/main.py mergePDFs

d: dev
dev:
	# nodemon --exec python src/main.py mergePDFs
	nodemon --exec python src/main.py makePDFs

# clean pdfs
clean:
	for dir in ./pdfs/*(/) ./pdfs/*/*(/) ./pdfs/*/*/*(/); do \
		if [[ -z $$(ls -A $$dir) ]]; then \
			rmdir $$dir; \
		fi; \
	done
