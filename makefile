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
