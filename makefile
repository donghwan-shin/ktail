install:
	pip install -r requirements.txt

clean:
	rm -f *.pdf tests/*.pdf
	rm -f *.dot tests/*.dot
	rm -f *.png tests/*.png

linter:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude venv
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude venv

test:
	pytest -v