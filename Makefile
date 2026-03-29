VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PROMPT = snoa

.PHONY: wheel clean venv test

venv: $(VENV)/bin/activate

$(VENV)/bin/activate:
	python3 -m venv --prompt $(PROMPT) $(VENV)
	$(PIP) install --upgrade pip wheel
	$(PIP) install -e ".[dev]"

wheel: venv
	$(PYTHON) -m build --wheel

test: venv
	$(PYTHON) -m pytest tests/ -v

clean:
	rm -rf dist/ build/ *.egg-info satnogs_network_api/*.egg-info
