SHELL := /bin/zsh

f: freeze
freeze:
	pip freeze > requirements.txt

i: install
install:
	pip install -r requirements.txt

r: run
run:
	python src/main.py t

r.s:
	python src/main.py t --skipDownload

# clean pdfs
clean:
	for dir in ./pdfs/*(/) ./pdfs/*/*(/) ./pdfs/*/*/*(/); do \
		if [[ -z $$(ls -A $$dir) ]]; then \
			rmdir $$dir; \
		fi; \
	done
