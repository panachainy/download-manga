SHELL := /bin/zsh

p: prepair
prepair:
	npm i -g nodemon
i:
	poetry install

sh:
	poetry shell

r: run
download: run
run:
	python src/cli.py download

load_config:
	python src/cli.py load_config

load_download:
	go run main.go

make:
	python src/cli.py makePDFs

merge: mergePDF
mergePDF:
	python src/cli.py mergePDFs

pdf:
	python src/cli.py makePDFs
	python src/cli.py mergePDFs

d: dev
dev:
	# nodemon --exec python -m streamlit run src/main.py 
	python -m streamlit run src/main.py 

# clean pdfs
clean:
	for dir in ./pdfs/*(/) ./pdfs/*/*(/) ./pdfs/*/*/*(/); do \
		if [[ -z $$(ls -A $$dir) ]]; then \
			rmdir $$dir; \
		fi; \
	done
