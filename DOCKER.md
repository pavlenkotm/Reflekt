# Docker Guide for Reflekt

Complete Docker setup for the Reflekt Web3 Multi-Language Repository.

## Quick Start

### Development Environment

Start a development shell with all languages installed:

```bash
docker-compose up -d dev
docker-compose exec dev bash
```

### Run All Tests

```bash
docker-compose up test
```

### Run Specific Language Tests

```bash
# Python tests
docker-compose up test-python

# TypeScript tests
docker-compose up test-typescript

# JavaScript tests
docker-compose up test-javascript

# Go tests
docker-compose up test-go

# Solidity tests
docker-compose up test-solidity
```

## Services

### Development (`dev`)
Full development environment with:
- Python 3.10
- Node.js 20
- Go 1.21
- Rust 1.75
- C++ (g++)

All project files are mounted, allowing live code changes.

### Testing (`test`)
Runs the complete test suite for all languages.

### API (`api`)
Python FastAPI backend service on port 8000.

### Frontend (`frontend`)
Streamlit web application on port 8501.

### Hardhat (`hardhat`)
Local Ethereum blockchain on port 8545.

## Common Commands

### Build Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build dev
```

### Start Services

```bash
# Start development environment
docker-compose up -d dev

# Start API and frontend
docker-compose up -d api frontend

# Start local blockchain
docker-compose up -d hardhat
```

### Execute Commands

```bash
# Run Python script
docker-compose exec dev python3 python/web3_cli.py --help

# Run TypeScript
docker-compose exec dev bash -c "cd typescript && npm start"

# Run Go program
docker-compose exec dev bash -c "cd go && go run signature_verifier.go"

# Compile Solidity
docker-compose exec dev bash -c "cd solidity && npx hardhat compile"
```

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs
docker-compose logs -f api

# View specific service
docker-compose logs frontend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# RPC Endpoint
WEB3_RPC_URL=https://eth.llamarpc.com

# Private key for transactions (optional)
PRIVATE_KEY=0x...

# API URL for frontend
API_URL=http://api:8000
```

## Development Workflow

### 1. Start Development Environment

```bash
docker-compose up -d dev
docker-compose exec dev bash
```

### 2. Make Changes

Edit files on your host machine. Changes are immediately reflected in the container.

### 3. Run Tests

```bash
# Inside container
cd python && pytest tests/
cd ../typescript && npm test
cd ../go && go test ./...
```

### 4. Run Linters

```bash
# Python
flake8 python/ src/

# TypeScript
cd typescript && npm run lint

# Go
cd go && go fmt ./...

# Rust
cd rust && cargo fmt
```

## Production Deployment

### Build Production Image

```bash
docker build -t reflekt-api:latest --target production .
```

### Run Production Container

```bash
docker run -d \
  -p 8000:8000 \
  -e WEB3_RPC_URL=https://eth.llamarpc.com \
  --name reflekt-api \
  reflekt-api:latest
```

## Testing with Local Blockchain

### 1. Start Hardhat Node

```bash
docker-compose up -d hardhat
```

### 2. Deploy Contracts

```bash
docker-compose exec dev bash
cd contracts
npx hardhat run scripts/deploy.js --network localhost
```

### 3. Update RPC URL

```bash
export WEB3_RPC_URL=http://hardhat:8545
```

## Troubleshooting

### Port Already in Use

```bash
# Change port in docker-compose.yml or stop conflicting service
lsof -ti:8000 | xargs kill -9
```

### Permission Denied

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Container Won't Start

```bash
# View logs
docker-compose logs dev

# Rebuild
docker-compose build --no-cache dev
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a --volumes
```

## Advanced Usage

### Custom Dockerfile Targets

```bash
# Build specific stage
docker build --target python-env -t reflekt-python .
docker build --target node-env -t reflekt-node .
docker build --target go-env -t reflekt-go .
```

### Multi-Architecture Build

```bash
# Build for ARM64 (M1 Mac) and AMD64
docker buildx build --platform linux/amd64,linux/arm64 -t reflekt:latest .
```

### Volume Management

```bash
# List volumes
docker volume ls

# Remove unused volumes
docker volume prune
```

## Performance Tips

1. **Use BuildKit**: `export DOCKER_BUILDKIT=1`
2. **Layer Caching**: Order Dockerfile commands from least to most frequently changing
3. **Multi-stage Builds**: Already implemented to reduce image size
4. **Volume Mounts**: Used for node_modules to speed up builds

## Security

1. **Never commit `.env` files** with private keys
2. **Use secrets management** in production (e.g., Docker secrets, AWS Secrets Manager)
3. **Run as non-root user** in production (add to Dockerfile if needed)
4. **Scan images** for vulnerabilities: `docker scan reflekt:latest`

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
