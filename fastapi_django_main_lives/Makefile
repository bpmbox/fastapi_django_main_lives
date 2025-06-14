#Sets the default shell for executing commands as /bin/bash and specifies command should be executed in a Bash shell.
SHELL := /bin/bash

# Color codes for terminal output
COLOR_RESET=\033[0m
COLOR_CYAN=\033[1;36m
COLOR_GREEN=\033[1;32m

# Defines the targets help, install, dev-install, and run as phony targets.
.PHONY: help install run dev debug app server test clean requirements ci-test ci-quick ci-full stop-port gui gui-auto gui-stop gui-logs gui-restart gui-simple

#sets the default goal to help when no target is specified on the command line.
.DEFAULT_GOAL := help

#Disables echoing of commands.
.SILENT:

#Sets the variable name to the second word from the MAKECMDGOALS.
name := $(word 2,$(MAKECMDGOALS))

#Defines a target named help.
help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo "  help           	Return this message with usage instructions."
	@echo "  install        	Will install the dependencies using Poetry."
	@echo "  run <folder_name>  Runs GPT Engineer on the folder with the given name."
	@echo "  app            	Run the main FastAPI application (app.py) - auto stops port 7860"
	@echo "  dev            	Run the application in development mode with hot reload - auto stops port 7860"
	@echo "  debug          	Run the application in debug mode (no reload) - auto stops port 7860"
	@echo "  server         	Run the ASGI server directly with uvicorn - auto stops port 7860"	@echo "  gui            	Start AI GUI Desktop Environment (http://localhost:6080)"
	@echo "  gui-auto       	Auto-start GUI with browser launch"
	@echo "  gui-simple     	Start simple GUI environment (http://localhost:6081)"
	@echo "  gui-stop       	Stop GUI Desktop Environment"
	@echo "  gui-restart    	Restart GUI Desktop Environment"
	@echo "  gui-logs       	Show GUI logs"
	@echo "  stop-port      	Stop any process running on port 7860"
	@echo "  ci-test        	Run CI/CD automated tests"
	@echo "  ci-quick       	Run quick CI test (no GitHub Issue)"
	@echo "  ci-full        	Run full CI pipeline with GitHub Issue"
	@echo "  ci-comprehensive	Run comprehensive controller tests"
	@echo "  ci-real-api      	Run real Gradio API tests"
	@echo "  test           	Run all tests"
	@echo "  requirements   	Install Python requirements from requirements.txt"
	@echo "  clean          	Clean up temporary files and caches"

#Defines a target named install. This target will install the project using Poetry.
install: poetry-install install-pre-commit farewell

#Defines a target named poetry-install. This target will install the project dependencies using Poetry.
poetry-install:
	@echo -e "$(COLOR_CYAN)Installing project with Poetry...$(COLOR_RESET)" && \
	poetry install

#Defines a target named install-pre-commit. This target will install the pre-commit hooks.
install-pre-commit:
	export OPENAI_API_BASE="https://api.groq.com/openai/v1/chat/completions"
	export OPENAI_API_KEY="sk-key-from-open-router"
	export MODEL_NAME="meta-llama/llama-3-8b-instruct:extended"
	export LOCAL_MODEL=true
	@echo -e "$(COLOR_CYAN)Installing pre-commit hooks...$(COLOR_RESET)" && \
	poetry run pre-commit install

#Defines a target named farewell. This target will print a farewell message.
farewell:
	@echo -e "$(COLOR_GREEN)All done!$(COLOR_RESET)"

#Defines a target named run. This target will run GPT Engineer on the folder with the given name.


runs:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer on $(COLOR_GREEN)$(name)$(COLOR_CYAN)...$(COLOR_RESET)"
	@cd ./gpt-engineer && \
	echo -e "y\ny\ny" | poetry run gpt-engineer "/home/user/app/controllers/$(name)" --model Llama3-70b-8192 --temperature 0.1
run:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer on $(COLOR_GREEN)$(name)$(COLOR_CYAN) folder...$(COLOR_RESET)" && \
	cd ./gpt-engineer && poetry run gpt-engineer /home/user/app/app/Http/controller/$(name) --model Llama3-70b-8192 --temperature 0.1

runbabyagi:
	cd ./babyagi && python babyagi.py $(name)

install:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer on $(COLOR_GREEN)$(name)$(COLOR_CYAN) folder...$(COLOR_RESET)" && \
	cd ./gpt-engineer && pip install poetry && make install


# Counts the lines of code in the project
cloc:
	cloc . --exclude-dir=node_modules,dist,build,.mypy_cache,benchmark --exclude-list-file=.gitignore --fullpath --not-match-d='docs/_build' --by-file

ssh:
	ssh-keygen -t rsa -b 4096 \-f ~/.ssh/id_rsa_new

# Application commands
stop-port:
	@echo -e "$(COLOR_CYAN)Stopping processes on port 7860...$(COLOR_RESET)"
	@if lsof -ti:7860 > /dev/null 2>&1; then \
		echo -e "$(COLOR_CYAN)Found process on port 7860, stopping...$(COLOR_RESET)"; \
		kill -9 $$(lsof -ti:7860) 2>/dev/null || true; \
		sleep 2; \
	else \
		echo -e "$(COLOR_GREEN)No process found on port 7860$(COLOR_RESET)"; \
	fi

app: stop-port
	@echo -e "$(COLOR_CYAN)Starting FastAPI application...$(COLOR_RESET)"
	SPACE_ID="" python app.py

dev: stop-port
	@echo -e "$(COLOR_CYAN)Starting application in development mode...$(COLOR_RESET)"
	SPACE_ID="" python app.py

debug: stop-port
	@echo -e "$(COLOR_CYAN)Starting application in debug mode...$(COLOR_RESET)"
	SPACE_ID="" python app.py --debug

server: stop-port
	@echo -e "$(COLOR_CYAN)Starting ASGI server directly...$(COLOR_RESET)"
	uvicorn mysite.asgi:app --host 0.0.0.0 --port 7860 --reload

# Requirements and dependencies
requirements:
	@echo -e "$(COLOR_CYAN)Installing Python requirements...$(COLOR_RESET)"
	pip install -r requirements.txt

# Testing
test:
	@echo -e "$(COLOR_CYAN)Running tests...$(COLOR_RESET)"
	python -m pytest tests/ -v

# Utility commands
clean:
	@echo -e "$(COLOR_CYAN)Cleaning up temporary files...$(COLOR_RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

# Database commands
migrate:
	@echo -e "$(COLOR_CYAN)Running database migrations...$(COLOR_RESET)"
	python manage.py migrate

makemigrations:
	@echo -e "$(COLOR_CYAN)Creating database migrations...$(COLOR_RESET)"
	python manage.py makemigrations

# Docker commands
docker-build:
	@echo -e "$(COLOR_CYAN)Building Docker image...$(COLOR_RESET)"
	docker-compose build

docker-up:
	@echo -e "$(COLOR_CYAN)Starting Docker containers...$(COLOR_RESET)"
	docker-compose up -d

docker-down:
	@echo -e "$(COLOR_CYAN)Stopping Docker containers...$(COLOR_RESET)"
	docker-compose down

# GUI commands
gui:
	@echo -e "$(COLOR_CYAN)Starting AI GUI Desktop Environment...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)GUI will be available at: http://localhost:6080$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)VNC direct access: localhost:5901$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)Default credentials: copilot/copilot$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml up -d

gui-auto:
	@echo -e "$(COLOR_CYAN)Auto-starting GUI with browser launch...$(COLOR_RESET)"
	./scripts/start_gui_auto.sh

gui-stop:
	@echo -e "$(COLOR_CYAN)Stopping GUI Desktop Environment...$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml down

gui-logs:
	@echo -e "$(COLOR_CYAN)Showing GUI logs...$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml logs -f

gui-restart:
	@echo -e "$(COLOR_CYAN)Restarting GUI Desktop Environment...$(COLOR_RESET)"
	docker-compose -f docker-ai-gui-desktop.yml restart

gui-simple:
	@echo -e "$(COLOR_CYAN)Starting simple GUI environment...$(COLOR_RESET)"
	@echo -e "$(COLOR_GREEN)GUI will be available at: http://localhost:6081$(COLOR_RESET)"
	docker-compose -f docker-compose-gui.yml up -d

# CI/CD commands
ci-test:
	@echo -e "$(COLOR_CYAN)Running CI/CD automated tests...$(COLOR_RESET)"
	chmod +x quick_ci_test.sh
	./quick_ci_test.sh

ci-quick:
	@echo -e "$(COLOR_CYAN)Running quick CI test (no GitHub Issue)...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py --no-github-issue

ci-full:
	@echo -e "$(COLOR_CYAN)Running full CI pipeline with GitHub Issue...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py

ci-verbose:
	@echo -e "$(COLOR_CYAN)Running CI pipeline with verbose output...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py --verbose

ci-comprehensive:
	@echo -e "$(COLOR_CYAN)Running comprehensive controller tests...$(COLOR_RESET)"
	python3 comprehensive_controller_test.py

ci-comprehensive-issue:
	@echo -e "$(COLOR_CYAN)Running comprehensive tests with GitHub Issue...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py --comprehensive

ci-real-api:
	@echo -e "$(COLOR_CYAN)Running real Gradio API tests...$(COLOR_RESET)"
	python3 real_gradio_api_tester.py

ci-all:
	@echo -e "$(COLOR_CYAN)Running all tests (comprehensive + real API + GitHub Issues)...$(COLOR_RESET)"
	python3 run_complete_ci_pipeline.py