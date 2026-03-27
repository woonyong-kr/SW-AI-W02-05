PYTHON := python3

.PHONY: all week2 week3 week4 week5

all: week2 week3 week4 week5

week2:
	@echo "=========================================="
	@echo "  Week 2 전체 테스트"
	@echo "=========================================="
	@cd week2/basic && $(PYTHON) check.py --all

week3:
	@echo "=========================================="
	@echo "  Week 3 전체 테스트"
	@echo "=========================================="
	@cd week3/basic && $(PYTHON) check.py --all

week4:
	@echo "=========================================="
	@echo "  Week 4 전체 테스트"
	@echo "=========================================="
	@cd week4/basic && $(PYTHON) check.py --all

week5:
	@echo "=========================================="
	@echo "  Week 5 전체 테스트"
	@echo "=========================================="
	@cd week5/basic && $(PYTHON) check.py --all
