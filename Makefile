run: install
	python3 MazeGenerator.py config.txt

install: frontend/mlx-2.2-py3-none-any.whl
	pip install frontend/mlx-2.2-py3-none-any.whl

debug: install
	venv/bin/python3 -m pdb a_maze_ing.py

clean:
	rm -rf backend/__pycache__ frontend/__pycache__

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# install in venv
dev-run: dev-install
	venv/bin/python3 a_maze_ing.py

dev-install: venv/bin/activate

venv/bin/activate: frontend/mlx-2.2-py3-none-any.whl
	python3 -m venv venv
	venv/bin/pip install frontend/mlx-2.2-py3-none-any.whl
