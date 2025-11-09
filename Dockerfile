# Multi-stage Dockerfile for Reflekt Web3 Multi-Language Repository
# Supports Python, TypeScript, JavaScript, Go, Rust, and more

FROM ubuntu:22.04 as base

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install common dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    cmake \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ===================================
# Python Environment
# ===================================
FROM base as python-env

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY python/requirements.txt ./python/

RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir -r python/requirements.txt

COPY python/ ./python/
COPY src/ ./src/

# ===================================
# Node.js Environment (TypeScript/JavaScript)
# ===================================
FROM base as node-env

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# TypeScript
COPY typescript/package*.json ./typescript/
RUN cd typescript && npm install

COPY typescript/ ./typescript/

# JavaScript
COPY javascript/package*.json ./javascript/
RUN cd javascript && npm install

COPY javascript/ ./javascript/

# Solidity
COPY solidity/package*.json ./solidity/
RUN cd solidity && npm install

COPY solidity/ ./solidity/

COPY contracts/package*.json ./contracts/
RUN cd contracts && npm install

COPY contracts/ ./contracts/

# ===================================
# Go Environment
# ===================================
FROM golang:1.21-bullseye as go-env

WORKDIR /app

COPY go/go.mod go/go.sum ./go/
RUN cd go && go mod download

COPY go/ ./go/

RUN cd go && go build -o signature_verifier .

# ===================================
# Rust Environment
# ===================================
FROM rust:1.75-bullseye as rust-env

WORKDIR /app

COPY rust/ ./rust/

RUN cd rust && cargo build --release

# ===================================
# Final Development Image
# ===================================
FROM base as development

# Install all language runtimes
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    nodejs \
    npm \
    golang-1.21 \
    rustc \
    cargo \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Node dependencies
RUN cd typescript && npm install && \
    cd ../javascript && npm install && \
    cd ../solidity && npm install && \
    cd ../contracts && npm install

# Install Go dependencies
RUN cd go && go mod download

# Set up environment
ENV PATH="/usr/lib/go-1.21/bin:${PATH}"
ENV GOPATH="/go"

# Default command
CMD ["/bin/bash"]

# ===================================
# Testing Image
# ===================================
FROM development as testing

WORKDIR /workspace

# Run all tests
CMD ["bash", "-c", "\
    echo '=== Running Python Tests ===' && \
    cd python && pytest tests/ --verbose && \
    cd ../src && pytest tests/ --verbose && \
    echo '=== Running TypeScript Tests ===' && \
    cd ../typescript && npm test && \
    echo '=== Running JavaScript Tests ===' && \
    cd ../javascript && npm test && \
    echo '=== Running Go Tests ===' && \
    cd ../go && go test -v ./... && \
    echo '=== Running Solidity Tests ===' && \
    cd ../solidity && npx hardhat test && \
    cd ../contracts && npx hardhat test && \
    echo '=== All Tests Passed ===' \
"]

# ===================================
# Production Image (Python API)
# ===================================
FROM python-env as production

WORKDIR /app

EXPOSE 8000

CMD ["python3", "src/api.py"]
