package token

import (
	"context"
	"testing"

	"cosmossdk.io/math"
	"cosmossdk.io/store"
	storetypes "cosmossdk.io/store/types"
	"github.com/cosmos/cosmos-sdk/codec"
	sdk "github.com/cosmos/cosmos-sdk/types"
	"github.com/stretchr/testify/require"
)

// setupTestKeeper creates a test keeper and context
func setupTestKeeper(t *testing.T) (TokenKeeper, sdk.Context) {
	storeKey := storetypes.NewKVStoreKey("token")

	db := store.NewCommitMultiStore(nil, nil)
	ctx := sdk.NewContext(db, false, nil)

	keeper := NewTokenKeeper(storeKey)

	return keeper, ctx
}

func TestGetSetBalance(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr := sdk.AccAddress("addr1")
	amount := math.NewInt(1000)

	// Initially balance should be zero
	balance := keeper.GetBalance(ctx, addr)
	require.True(t, balance.IsZero())

	// Set balance
	err := keeper.SetBalance(ctx, addr, amount)
	require.NoError(t, err)

	// Check balance
	balance = keeper.GetBalance(ctx, addr)
	require.Equal(t, amount, balance)
}

func TestSetBalanceNegative(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr := sdk.AccAddress("addr1")
	amount := math.NewInt(-100)

	err := keeper.SetBalance(ctx, addr, amount)
	require.Error(t, err)
	require.Contains(t, err.Error(), "amount cannot be negative")
}

func TestTransfer(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	from := sdk.AccAddress("from")
	to := sdk.AccAddress("to")
	amount := math.NewInt(100)

	// Set initial balance for sender
	err := keeper.SetBalance(ctx, from, math.NewInt(1000))
	require.NoError(t, err)

	// Transfer
	err = keeper.Transfer(ctx, from, to, amount)
	require.NoError(t, err)

	// Check balances
	fromBalance := keeper.GetBalance(ctx, from)
	require.Equal(t, math.NewInt(900), fromBalance)

	toBalance := keeper.GetBalance(ctx, to)
	require.Equal(t, amount, toBalance)
}

func TestTransferInsufficientFunds(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	from := sdk.AccAddress("from")
	to := sdk.AccAddress("to")
	amount := math.NewInt(100)

	// Set initial balance (less than transfer amount)
	err := keeper.SetBalance(ctx, from, math.NewInt(50))
	require.NoError(t, err)

	// Transfer should fail
	err = keeper.Transfer(ctx, from, to, amount)
	require.Error(t, err)
	require.Contains(t, err.Error(), "insufficient balance")
}

func TestTransferZeroAmount(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	from := sdk.AccAddress("from")
	to := sdk.AccAddress("to")
	amount := math.ZeroInt()

	err := keeper.Transfer(ctx, from, to, amount)
	require.Error(t, err)
	require.Contains(t, err.Error(), "transfer amount must be positive")
}

func TestMint(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr := sdk.AccAddress("addr1")
	amount := math.NewInt(500)

	// Mint tokens
	err := keeper.Mint(ctx, addr, amount)
	require.NoError(t, err)

	// Check balance
	balance := keeper.GetBalance(ctx, addr)
	require.Equal(t, amount, balance)

	// Mint more tokens
	err = keeper.Mint(ctx, addr, amount)
	require.NoError(t, err)

	// Check updated balance
	balance = keeper.GetBalance(ctx, addr)
	require.Equal(t, math.NewInt(1000), balance)
}

func TestMintZeroAmount(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr := sdk.AccAddress("addr1")
	amount := math.ZeroInt()

	err := keeper.Mint(ctx, addr, amount)
	require.Error(t, err)
	require.Contains(t, err.Error(), "mint amount must be positive")
}

func TestBurn(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr := sdk.AccAddress("addr1")
	initialAmount := math.NewInt(1000)
	burnAmount := math.NewInt(300)

	// Set initial balance
	err := keeper.SetBalance(ctx, addr, initialAmount)
	require.NoError(t, err)

	// Burn tokens
	err = keeper.Burn(ctx, addr, burnAmount)
	require.NoError(t, err)

	// Check balance
	balance := keeper.GetBalance(ctx, addr)
	require.Equal(t, math.NewInt(700), balance)
}

func TestBurnInsufficientBalance(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr := sdk.AccAddress("addr1")
	burnAmount := math.NewInt(500)

	// Set initial balance (less than burn amount)
	err := keeper.SetBalance(ctx, addr, math.NewInt(300))
	require.NoError(t, err)

	// Burn should fail
	err = keeper.Burn(ctx, addr, burnAmount)
	require.Error(t, err)
	require.Contains(t, err.Error(), "insufficient balance")
}

func TestGetTotalSupply(t *testing.T) {
	keeper, ctx := setupTestKeeper(t)

	addr1 := sdk.AccAddress("addr1")
	addr2 := sdk.AccAddress("addr2")

	// Set balances
	err := keeper.SetBalance(ctx, addr1, math.NewInt(1000))
	require.NoError(t, err)

	err = keeper.SetBalance(ctx, addr2, math.NewInt(500))
	require.NoError(t, err)

	// Check total supply
	totalSupply := keeper.GetTotalSupply(ctx)
	require.Equal(t, math.NewInt(1500), totalSupply)
}

// Message validation tests
func TestTransferMsgValidateBasic(t *testing.T) {
	tests := []struct {
		name    string
		msg     TransferMsg
		wantErr bool
	}{
		{
			name: "valid message",
			msg: TransferMsg{
				From:   "cosmos1...",
				To:     "cosmos2...",
				Amount: "1000",
			},
			wantErr: false,
		},
		{
			name: "empty from",
			msg: TransferMsg{
				From:   "",
				To:     "cosmos2...",
				Amount: "1000",
			},
			wantErr: true,
		},
		{
			name: "empty to",
			msg: TransferMsg{
				From:   "cosmos1...",
				To:     "",
				Amount: "1000",
			},
			wantErr: true,
		},
		{
			name: "empty amount",
			msg: TransferMsg{
				From:   "cosmos1...",
				To:     "cosmos2...",
				Amount: "",
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.msg.ValidateBasic()
			if tt.wantErr {
				require.Error(t, err)
			} else {
				require.NoError(t, err)
			}
		})
	}
}

func TestMintMsgValidateBasic(t *testing.T) {
	tests := []struct {
		name    string
		msg     MintMsg
		wantErr bool
	}{
		{
			name: "valid message",
			msg: MintMsg{
				Recipient: "cosmos1...",
				Amount:    "1000",
			},
			wantErr: false,
		},
		{
			name: "empty recipient",
			msg: MintMsg{
				Recipient: "",
				Amount:    "1000",
			},
			wantErr: true,
		},
		{
			name: "empty amount",
			msg: MintMsg{
				Recipient: "cosmos1...",
				Amount:    "",
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.msg.ValidateBasic()
			if tt.wantErr {
				require.Error(t, err)
			} else {
				require.NoError(t, err)
			}
		})
	}
}

func TestBurnMsgValidateBasic(t *testing.T) {
	tests := []struct {
		name    string
		msg     BurnMsg
		wantErr bool
	}{
		{
			name: "valid message",
			msg: BurnMsg{
				Burner: "cosmos1...",
				Amount: "1000",
			},
			wantErr: false,
		},
		{
			name: "empty burner",
			msg: BurnMsg{
				Burner: "",
				Amount: "1000",
			},
			wantErr: true,
		},
		{
			name: "empty amount",
			msg: BurnMsg{
				Burner: "cosmos1...",
				Amount: "",
			},
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			err := tt.msg.ValidateBasic()
			if tt.wantErr {
				require.Error(t, err)
			} else {
				require.NoError(t, err)
			}
		})
	}
}
