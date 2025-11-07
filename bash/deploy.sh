#!/bin/bash

#########################################
# Web3 Deployment Automation Script
# Handles smart contract deployment, verification, and monitoring
#########################################

set -e  # Exit on error
set -u  # Error on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NETWORK=${NETWORK:-"sepolia"}
PRIVATE_KEY=${PRIVATE_KEY:-""}
RPC_URL=${RPC_URL:-"https://eth.llamarpc.com"}
CONTRACT_DIR="./contracts"
DEPLOYMENT_LOG="./deployments/${NETWORK}.json"

#########################################
# Helper Functions
#########################################

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

#########################################
# Validation
#########################################

validate_environment() {
    log_info "Validating environment..."

    # Check required tools
    check_command "node"
    check_command "npx"
    check_command "jq"

    # Check private key
    if [ -z "$PRIVATE_KEY" ]; then
        log_error "PRIVATE_KEY environment variable is not set"
        exit 1
    fi

    # Check RPC connection
    if ! curl -s "$RPC_URL" --max-time 5 &> /dev/null; then
        log_warning "Cannot reach RPC endpoint: $RPC_URL"
    fi

    log_success "Environment validation complete"
}

#########################################
# Contract Compilation
#########################################

compile_contracts() {
    log_info "Compiling smart contracts..."

    cd "$CONTRACT_DIR" || exit 1

    if [ -f "hardhat.config.js" ]; then
        npx hardhat compile
    elif [ -f "foundry.toml" ]; then
        forge build
    else
        log_error "No Hardhat or Foundry config found"
        exit 1
    fi

    cd - > /dev/null

    log_success "Contracts compiled successfully"
}

#########################################
# Deployment
#########################################

deploy_contracts() {
    log_info "Deploying contracts to $NETWORK..."

    # Create deployments directory
    mkdir -p "$(dirname "$DEPLOYMENT_LOG")"

    # Deploy with Hardhat
    if [ -f "$CONTRACT_DIR/hardhat.config.js" ]; then
        cd "$CONTRACT_DIR" || exit 1
        npx hardhat run scripts/deploy.js --network "$NETWORK" | tee /tmp/deploy.log
        cd - > /dev/null

        # Extract contract address from deployment output
        CONTRACT_ADDRESS=$(grep -oP '(?<=deployed to: )\w+' /tmp/deploy.log | head -1)

        if [ -n "$CONTRACT_ADDRESS" ]; then
            log_success "Contract deployed at: $CONTRACT_ADDRESS"

            # Save deployment info
            cat > "$DEPLOYMENT_LOG" << EOF
{
  "network": "$NETWORK",
  "contractAddress": "$CONTRACT_ADDRESS",
  "deployedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "deployer": "$(cast wallet address $PRIVATE_KEY 2>/dev/null || echo 'unknown')",
  "chainId": "$(cast chain-id --rpc-url $RPC_URL 2>/dev/null || echo 'unknown')"
}
EOF
        else
            log_error "Failed to extract contract address"
            exit 1
        fi
    fi

    log_success "Deployment complete"
}

#########################################
# Contract Verification
#########################################

verify_contract() {
    local CONTRACT_ADDRESS=$1

    log_info "Verifying contract on Etherscan..."

    if [ -f "$CONTRACT_DIR/hardhat.config.js" ]; then
        cd "$CONTRACT_DIR" || exit 1
        npx hardhat verify --network "$NETWORK" "$CONTRACT_ADDRESS" || {
            log_warning "Verification failed (this is normal if already verified)"
        }
        cd - > /dev/null
    fi

    log_success "Verification process complete"
}

#########################################
# Post-Deployment Actions
#########################################

post_deployment_checks() {
    log_info "Running post-deployment checks..."

    if [ -f "$DEPLOYMENT_LOG" ]; then
        CONTRACT_ADDRESS=$(jq -r '.contractAddress' "$DEPLOYMENT_LOG")

        # Check contract code
        CODE=$(cast code "$CONTRACT_ADDRESS" --rpc-url "$RPC_URL" 2>/dev/null || echo "0x")

        if [ "$CODE" != "0x" ] && [ "$CODE" != "" ]; then
            log_success "Contract code verified on-chain"
        else
            log_error "No code found at contract address"
            exit 1
        fi

        # Display deployment summary
        echo ""
        log_info "Deployment Summary:"
        echo "================================"
        cat "$DEPLOYMENT_LOG" | jq .
        echo "================================"
    fi

    log_success "Post-deployment checks complete"
}

#########################################
# Gas Monitoring
#########################################

check_gas_price() {
    log_info "Checking current gas prices..."

    GAS_PRICE=$(cast gas-price --rpc-url "$RPC_URL" 2>/dev/null || echo "0")

    if [ "$GAS_PRICE" != "0" ]; then
        GAS_GWEI=$(echo "scale=2; $GAS_PRICE / 1000000000" | bc)
        log_info "Current gas price: ${GAS_GWEI} Gwei"

        # Warning for high gas
        if (( $(echo "$GAS_GWEI > 50" | bc -l) )); then
            log_warning "Gas price is high! Consider waiting."
        fi
    fi
}

#########################################
# Main Execution
#########################################

main() {
    echo ""
    log_info "🚀 Web3 Deployment Script"
    echo "================================"
    log_info "Network: $NETWORK"
    log_info "RPC URL: $RPC_URL"
    echo "================================"
    echo ""

    # Run deployment steps
    validate_environment
    check_gas_price
    compile_contracts
    deploy_contracts

    # Extract contract address for verification
    if [ -f "$DEPLOYMENT_LOG" ]; then
        CONTRACT_ADDRESS=$(jq -r '.contractAddress' "$DEPLOYMENT_LOG")
        verify_contract "$CONTRACT_ADDRESS"
    fi

    post_deployment_checks

    echo ""
    log_success "🎉 Deployment pipeline complete!"
    echo ""
}

# Run main function
main "$@"
