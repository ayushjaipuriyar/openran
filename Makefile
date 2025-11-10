# Makefile for OpenRAN Experiments

.PHONY: help benign benign-generate benign-run malicious malicious-generate malicious-run clean setup dataset

# Default target
help:
	@echo "Available targets:"
	@echo "  setup       - Install Python dependencies"
	@echo "  dataset     - Show dataset folder contents and info"
	@echo "  benign      - Generate and run benign experiments"
	@echo "  benign-generate [SEED=] [P=] - Generate benign experiments with optional seed and p parameters"
	@echo "  benign-run [START_TR=] [START_EXP=] - Run benign experiments from specific training set/experiment"
	@echo "  malicious   - Generate and run malicious experiments"
	@echo "  malicious-generate [SEED=] [P=] - Generate malicious experiments with optional seed and p parameters"
	@echo "  malicious-run [START_TR=] [START_EXP=] - Run malicious experiments from specific training set/experiment"
	@echo "  clean       - Clean generated experiment directories"
	@echo "  help        - Show this help message"
# Generate benign experiments
benign-generate:
	cd scripts && python generate_experiments.py $(if $(SEED),--seed $(SEED)) $(if $(P),--p $(P))

# Run benign experiments
benign-run:
	./scripts/run_benign.sh $(START_TR) $(START_EXP)

# Full benign workflow
benign: benign-generate benign-run

# Generate malicious experiments
malicious-generate:
	cd scripts && python generate_malicious_experiments.py $(if $(SEED),--seed $(SEED)) $(if $(P),--p $(P))

# Run malicious experiments
malicious-run:
	./scripts/run_malicious.sh $(START_TR) $(START_EXP)

# Full malicious workflow
malicious: malicious-generate malicious-run

# Clean generated directories
clean:
	rm -rf generated_experiments generated_malicious_experiments

# Clean Python cache
clean-cache:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Show dataset information
dataset:
	@echo "Dataset folder contents:"
	@ls -la dataset/
	@echo ""
	@echo "Dataset README:"
	@cat dataset/README.md
