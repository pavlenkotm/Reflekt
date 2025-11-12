# 🌌 Cosmos SDK - Token Module

A production-ready token module built with Cosmos SDK, demonstrating the framework's modular architecture for building custom blockchains.

## 📋 Overview

Cosmos SDK is a modular framework for building application-specific blockchains. This example implements a custom token module showcasing:

- **Keeper Pattern**: State management with TokenKeeper
- **Context Usage**: SDK context for transaction processing
- **Event Emission**: Blockchain events for indexing
- **Message Validation**: Input validation with ValidateBasic
- **State Persistence**: KVStore for efficient storage
- **Testing**: Comprehensive unit tests

## ✨ Key Features

- ✅ **Transfer Tokens**: Send tokens between accounts
- ✅ **Mint Tokens**: Create new tokens (with access control in production)
- ✅ **Burn Tokens**: Destroy tokens from circulation
- ✅ **Query Balances**: Check account balances
- ✅ **Total Supply**: Calculate total token supply
- ✅ **Event Emission**: Emit events for all state changes
- ✅ **Error Handling**: Proper error messages and validation
- ✅ **Type Safety**: Strongly typed with Go

## 📁 Project Structure

```
cosmos-sdk/
├── token.go           # TokenKeeper and core logic
├── token_test.go      # Comprehensive test suite
├── go.mod             # Go module definition
└── README.md          # This file
```

## 🚀 Installation

### Prerequisites

```bash
# Install Go 1.21+
curl -OL https://go.dev/dl/go1.21.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz

# Add to PATH
export PATH=$PATH:/usr/local/go/bin
```

### Install Dependencies

```bash
cd cosmos-sdk
go mod download
```

## 🧪 Testing

```bash
# Run all tests
go test -v

# Run with coverage
go test -cover -coverprofile=coverage.out

# View coverage report
go tool cover -html=coverage.out

# Run specific test
go test -run TestTransfer -v

# Benchmark
go test -bench=.
```

## 📖 API Reference

### TokenKeeper

Main keeper for managing token state.

#### NewTokenKeeper

```go
func NewTokenKeeper(storeKey sdk.StoreKey) TokenKeeper
```

Creates a new TokenKeeper instance.

#### GetBalance

```go
func (k TokenKeeper) GetBalance(ctx context.Context, addr sdk.AccAddress) math.Int
```

Returns the token balance of an account.

**Example:**
```go
balance := keeper.GetBalance(ctx, addr)
fmt.Printf("Balance: %s\n", balance.String())
```

#### SetBalance

```go
func (k TokenKeeper) SetBalance(ctx context.Context, addr sdk.AccAddress, amount math.Int) error
```

Sets the balance of an account. Returns error if amount is negative.

**Example:**
```go
err := keeper.SetBalance(ctx, addr, math.NewInt(1000))
if err != nil {
    return err
}
```

#### Transfer

```go
func (k TokenKeeper) Transfer(ctx context.Context, from, to sdk.AccAddress, amount math.Int) error
```

Transfers tokens from one account to another.

**Example:**
```go
err := keeper.Transfer(ctx, fromAddr, toAddr, math.NewInt(100))
if err != nil {
    return err
}
```

**Events Emitted:**
```go
sdk.NewEvent(
    "transfer",
    sdk.NewAttribute("from", from.String()),
    sdk.NewAttribute("to", to.String()),
    sdk.NewAttribute("amount", amount.String()),
)
```

#### Mint

```go
func (k TokenKeeper) Mint(ctx context.Context, addr sdk.AccAddress, amount math.Int) error
```

Mints new tokens to an account.

**Example:**
```go
err := keeper.Mint(ctx, recipientAddr, math.NewInt(500))
if err != nil {
    return err
}
```

**Events Emitted:**
```go
sdk.NewEvent(
    "mint",
    sdk.NewAttribute("recipient", addr.String()),
    sdk.NewAttribute("amount", amount.String()),
)
```

#### Burn

```go
func (k TokenKeeper) Burn(ctx context.Context, addr sdk.AccAddress, amount math.Int) error
```

Burns tokens from an account.

**Example:**
```go
err := keeper.Burn(ctx, burnerAddr, math.NewInt(200))
if err != nil {
    return err
}
```

**Events Emitted:**
```go
sdk.NewEvent(
    "burn",
    sdk.NewAttribute("burner", addr.String()),
    sdk.NewAttribute("amount", amount.String()),
)
```

#### GetTotalSupply

```go
func (k TokenKeeper) GetTotalSupply(ctx context.Context) math.Int
```

Returns the total token supply by iterating all account balances.

**Example:**
```go
totalSupply := keeper.GetTotalSupply(ctx)
fmt.Printf("Total Supply: %s\n", totalSupply.String())
```

## 💡 Message Types

### TransferMsg

```go
type TransferMsg struct {
    From   string `json:"from"`
    To     string `json:"to"`
    Amount string `json:"amount"`
}

func (msg TransferMsg) ValidateBasic() error
```

### MintMsg

```go
type MintMsg struct {
    Recipient string `json:"recipient"`
    Amount    string `json:"amount"`
}

func (msg MintMsg) ValidateBasic() error
```

### BurnMsg

```go
type BurnMsg struct {
    Burner string `json:"burner"`
    Amount string `json:"amount"`
}

func (msg BurnMsg) ValidateBasic() error
```

## 🔧 Integration Examples

### Creating a Full Module

```go
package token

import (
    sdk "github.com/cosmos/cosmos-sdk/types"
    "github.com/cosmos/cosmos-sdk/types/module"
)

// AppModule implements module.AppModule
type AppModule struct {
    keeper TokenKeeper
}

// Route returns the message routing key
func (am AppModule) Route() sdk.Route {
    return sdk.NewRoute("token", NewHandler(am.keeper))
}

// QuerierRoute returns the querier routing key
func (am AppModule) QuerierRoute() string {
    return "token"
}

// NewHandler creates a new message handler
func NewHandler(k TokenKeeper) sdk.Handler {
    return func(ctx sdk.Context, msg sdk.Msg) (*sdk.Result, error) {
        switch msg := msg.(type) {
        case *TransferMsg:
            return handleTransfer(ctx, k, msg)
        case *MintMsg:
            return handleMint(ctx, k, msg)
        case *BurnMsg:
            return handleBurn(ctx, k, msg)
        default:
            return nil, sdkerrors.ErrUnknownRequest
        }
    }
}
```

### Message Handlers

```go
func handleTransfer(ctx sdk.Context, k TokenKeeper, msg *TransferMsg) (*sdk.Result, error) {
    if err := msg.ValidateBasic(); err != nil {
        return nil, err
    }

    from, err := sdk.AccAddressFromBech32(msg.From)
    if err != nil {
        return nil, err
    }

    to, err := sdk.AccAddressFromBech32(msg.To)
    if err != nil {
        return nil, err
    }

    amount, ok := math.NewIntFromString(msg.Amount)
    if !ok {
        return nil, sdkerrors.ErrInvalidRequest.Wrap("invalid amount")
    }

    if err := k.Transfer(ctx, from, to, amount); err != nil {
        return nil, err
    }

    return &sdk.Result{Events: ctx.EventManager().ABCIEvents()}, nil
}
```

### CLI Integration

```go
package cli

import (
    "github.com/cosmos/cosmos-sdk/client"
    "github.com/cosmos/cosmos-sdk/client/flags"
    "github.com/cosmos/cosmos-sdk/client/tx"
    "github.com/spf13/cobra"
)

// GetTxCmd returns the transaction commands for the module
func GetTxCmd() *cobra.Command {
    cmd := &cobra.Command{
        Use:   "token",
        Short: "Token transaction subcommands",
    }

    cmd.AddCommand(
        GetCmdTransfer(),
        GetCmdMint(),
        GetCmdBurn(),
    )

    return cmd
}

// GetCmdTransfer returns the transfer command
func GetCmdTransfer() *cobra.Command {
    cmd := &cobra.Command{
        Use:   "transfer [to_address] [amount]",
        Short: "Transfer tokens to another account",
        Args:  cobra.ExactArgs(2),
        RunE: func(cmd *cobra.Command, args []string) error {
            clientCtx, err := client.GetClientTxContext(cmd)
            if err != nil {
                return err
            }

            msg := &TransferMsg{
                From:   clientCtx.GetFromAddress().String(),
                To:     args[0],
                Amount: args[1],
            }

            if err := msg.ValidateBasic(); err != nil {
                return err
            }

            return tx.GenerateOrBroadcastTxCLI(clientCtx, cmd.Flags(), msg)
        },
    }

    flags.AddTxFlagsToCmd(cmd)
    return cmd
}
```

### Query Server

```go
package keeper

import (
    "context"

    sdk "github.com/cosmos/cosmos-sdk/types"
)

type QueryServer struct {
    Keeper TokenKeeper
}

// Balance implements the Query/Balance gRPC method
func (q QueryServer) Balance(
    goCtx context.Context,
    req *QueryBalanceRequest,
) (*QueryBalanceResponse, error) {
    if req == nil {
        return nil, status.Error(codes.InvalidArgument, "empty request")
    }

    addr, err := sdk.AccAddressFromBech32(req.Address)
    if err != nil {
        return nil, err
    }

    ctx := sdk.UnwrapSDKContext(goCtx)
    balance := q.Keeper.GetBalance(ctx, addr)

    return &QueryBalanceResponse{
        Balance: balance.String(),
    }, nil
}

// TotalSupply implements the Query/TotalSupply gRPC method
func (q QueryServer) TotalSupply(
    goCtx context.Context,
    req *QueryTotalSupplyRequest,
) (*QueryTotalSupplyResponse, error) {
    ctx := sdk.UnwrapSDKContext(goCtx)
    totalSupply := q.Keeper.GetTotalSupply(ctx)

    return &QueryTotalSupplyResponse{
        TotalSupply: totalSupply.String(),
    }, nil
}
```

## 🏗️ Building a Blockchain

### 1. Initialize Chain

```bash
# Initialize chain configuration
appd init mychain --chain-id my-chain-1

# Add genesis accounts
appd keys add alice
appd keys add bob

appd add-genesis-account alice 1000000stake
appd add-genesis-account bob 1000000stake

# Create genesis transaction
appd gentx alice 100000stake --chain-id my-chain-1

# Collect genesis transactions
appd collect-gentxs

# Start chain
appd start
```

### 2. Send Transactions

```bash
# Transfer tokens
appd tx token transfer cosmos1... 1000 \
  --from alice \
  --chain-id my-chain-1 \
  --fees 500stake

# Mint tokens (if authorized)
appd tx token mint cosmos1... 5000 \
  --from alice \
  --chain-id my-chain-1

# Burn tokens
appd tx token burn 500 \
  --from alice \
  --chain-id my-chain-1
```

### 3. Query State

```bash
# Query balance
appd query token balance cosmos1...

# Query total supply
appd query token total-supply

# Query with gRPC
grpcurl -plaintext \
  -d '{"address": "cosmos1..."}' \
  localhost:9090 \
  token.Query/Balance
```

## 🔒 Security Best Practices

1. **✅ Access Control**
   ```go
   func (k TokenKeeper) Mint(ctx context.Context, addr sdk.AccAddress, amount math.Int) error {
       // Check if caller has minter role
       if !k.HasMinterRole(ctx, k.GetCaller(ctx)) {
           return sdkerrors.ErrUnauthorized.Wrap("caller is not a minter")
       }
       // ... rest of logic
   }
   ```

2. **✅ Input Validation**
   ```go
   if amount.IsNegative() || amount.IsZero() {
       return sdkerrors.ErrInvalidRequest.Wrap("amount must be positive")
   }
   ```

3. **✅ Integer Overflow Protection**
   - Cosmos SDK's `math.Int` type prevents overflow
   - Always use `math.Int` for amounts

4. **✅ Atomic Operations**
   - All state changes in a transaction are atomic
   - Failed transactions automatically rollback

5. **✅ Event Emission**
   ```go
   ctx.EventManager().EmitEvent(
       sdk.NewEvent("transfer", attrs...),
   )
   ```

## ⚡ Performance Tips

1. **Use Efficient Storage Keys**
   ```go
   // Good: Predictable key structure
   balanceKey := []byte(fmt.Sprintf("balance:%s", addr))

   // Better: Use key prefixes
   const BalancePrefix = 0x01
   balanceKey := append([]byte{BalancePrefix}, addr...)
   ```

2. **Batch Operations**
   ```go
   func (k TokenKeeper) BatchTransfer(
       ctx context.Context,
       transfers []Transfer,
   ) error {
       for _, t := range transfers {
           if err := k.Transfer(ctx, t.From, t.To, t.Amount); err != nil {
               return err
           }
       }
       return nil
   }
   ```

3. **Caching**
   ```go
   // Cache frequently accessed data
   ctx = ctx.WithCache()
   defer ctx.CommitCache()
   ```

4. **Limit Iterations**
   ```go
   // Use pagination for large datasets
   func (k TokenKeeper) GetTopHolders(ctx context.Context, limit int) []Holder
   ```

## 🆚 Cosmos SDK vs Other Frameworks

| Feature | Cosmos SDK | Ethereum | Polkadot |
|---------|------------|----------|----------|
| Language | Go | Solidity | Rust |
| Architecture | Modular | Monolithic | Modular |
| Consensus | Tendermint | PoS | NPoS |
| Scalability | ⚡ High | Moderate | ⚡ High |
| Interoperability | IBC | Bridges | XCM |
| Customization | ✅ Full | Limited | ✅ Full |
| Learning Curve | Moderate | Easy | Steep |
| Tooling | Mature | Excellent | Growing |

## 🌐 Cosmos Ecosystem

### Major Chains Using Cosmos SDK

- **Cosmos Hub**: First IBC-enabled chain
- **Osmosis**: DEX and AMM protocol
- **Terra**: Algorithmic stablecoin platform
- **Cronos**: Crypto.com chain
- **Kava**: DeFi lending platform
- **Akash**: Decentralized cloud computing
- **Celestia**: Modular blockchain network
- **dYdX**: Decentralized exchange

### IBC (Inter-Blockchain Communication)

```go
// Send tokens via IBC
func (k TokenKeeper) IBCTransfer(
    ctx sdk.Context,
    sourcePort, sourceChannel string,
    token sdk.Coin,
    sender, receiver string,
    timeoutHeight clienttypes.Height,
) error {
    // IBC transfer logic
}
```

## 📄 License

MIT License - see [LICENSE](../../LICENSE) for details

## 🔗 Resources

- **Cosmos SDK Docs**: https://docs.cosmos.network/
- **Tutorials**: https://tutorials.cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Discord**: https://discord.gg/cosmosnetwork
- **Cosmos Academy**: https://academy.cosmos.network/
- **IBC Protocol**: https://ibcprotocol.org/
- **Tendermint Core**: https://docs.tendermint.com/
- **CosmWasm**: https://cosmwasm.com/ (Rust smart contracts)

## 🎓 Learning Path

1. **Cosmos Basics**: https://cosmos.network/intro
2. **Build a Module**: https://tutorials.cosmos.network/tutorials/4-my-own-chain/
3. **IBC Integration**: https://tutorials.cosmos.network/tutorials/7-ibc/
4. **Deploy Testnet**: https://hub.cosmos.network/main/getting-started/
5. **CosmWasm Contracts**: https://book.cosmwasm.com/

---

**Built with ❤️ for the Interchain**
