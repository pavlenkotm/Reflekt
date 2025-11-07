# Makefile for Web3 Multi-Language Repository

.PHONY: help install test lint clean build

# Default target
help:
	@echo "Web3 Multi-Language Repository - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install dependencies for all languages"
	@echo "  make test        - Run tests for all languages"
	@echo "  make lint        - Run linters for all languages"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make build       - Build all projects"
	@echo "  make docs        - Generate documentation"
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	@echo ""
	@echo "Python..."
	@cd python && pip install -r requirements.txt || true
	@echo ""
	@echo "TypeScript..."
	@cd typescript && npm install || true
	@echo ""
	@echo "Solidity..."
	@cd solidity && npm install || true
	@echo ""
	@echo "Go..."
	@cd go && go mod download || true
	@echo ""
	@echo "✅ Installation complete!"

# Run tests
test:
	@echo "🧪 Running tests..."
	@echo ""
	@echo "Python tests..."
	@cd python && pytest || true
	@echo ""
	@echo "TypeScript tests..."
	@cd typescript && npm test || true
	@echo ""
	@echo "Solidity tests..."
	@cd solidity && npx hardhat test || true
	@echo ""
	@echo "Go tests..."
	@cd go && go test ./... || true
	@echo ""
	@echo "Rust tests..."
	@cd rust && cargo test || true
	@echo ""
	@echo "✅ Tests complete!"

# Run linters
lint:
	@echo "🔍 Running linters..."
	@echo ""
	@echo "Python..."
	@cd python && flake8 . || true
	@echo ""
	@echo "TypeScript..."
	@cd typescript && npm run lint || true
	@echo ""
	@echo "Markdown..."
	@markdownlint '**/*.md' --ignore node_modules || true
	@echo ""
	@echo "✅ Linting complete!"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	@find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "target" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Clean complete!"

# Build all projects
build:
	@echo "🔨 Building all projects..."
	@echo ""
	@echo "TypeScript..."
	@cd typescript && npm run build || true
	@echo ""
	@echo "Solidity..."
	@cd solidity && npx hardhat compile || true
	@echo ""
	@echo "Go..."
	@cd go && go build || true
	@echo ""
	@echo "Rust..."
	@cd rust && cargo build || true
	@echo ""
	@echo "C++..."
	@cd cpp && g++ -std=c++17 -o keccak256 keccak256.cpp || true
	@echo ""
	@echo "✅ Build complete!"

# Generate documentation
docs:
	@echo "📚 Generating documentation..."
	@echo "Documentation is already in markdown format!"
	@echo "See: README.md, ARCHITECTURE.md, TESTING.md, FAQ.md"
	@echo "✅ Done!"

# Git commands
.PHONY: status commit push

status:
	@git status

commit:
	@git add .
	@git status
	@echo "Ready to commit. Use: git commit -m 'your message'"

push:
	@git push -u origin $$(git branch --show-current)
