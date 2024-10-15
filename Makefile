.phony: run


run:
	@echo "Running the bot..."
	@python3 src/main.py

test:
	@echo "Running tests..."
	@pytest ./tests
