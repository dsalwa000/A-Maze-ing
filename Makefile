run: install
	python3 a_maze_ing.py config.txt

install: mlx-2.2-py3-none-any.whl
	pip install mlx-2.2-py3-none-any.whl

debug: install
	venv/bin/python3 -m pdb a_maze_ing.py

clean:
	rm -rf *__pycache__

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
