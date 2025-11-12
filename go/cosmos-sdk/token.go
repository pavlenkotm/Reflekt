package token

import (
	"context"
	"fmt"

	"cosmossdk.io/math"
	sdk "github.com/cosmos/cosmos-sdk/types"
	sdkerrors "github.com/cosmos/cosmos-sdk/types/errors"
)

// TokenKeeper manages token balances and operations
type TokenKeeper struct {
	storeKey sdk.StoreKey
}

// NewTokenKeeper creates a new TokenKeeper
func NewTokenKeeper(storeKey sdk.StoreKey) TokenKeeper {
	return TokenKeeper{
		storeKey: storeKey,
	}
}

// GetBalance returns the balance of an account
func (k TokenKeeper) GetBalance(ctx context.Context, addr sdk.AccAddress) math.Int {
	sdkCtx := sdk.UnwrapSDKContext(ctx)
	store := sdkCtx.KVStore(k.storeKey)

	bz := store.Get(addr)
	if bz == nil {
		return math.ZeroInt()
	}

	var balance math.Int
	if err := balance.Unmarshal(bz); err != nil {
		return math.ZeroInt()
	}

	return balance
}

// SetBalance sets the balance of an account
func (k TokenKeeper) SetBalance(ctx context.Context, addr sdk.AccAddress, amount math.Int) error {
	if amount.IsNegative() {
		return sdkerrors.ErrInvalidRequest.Wrap("amount cannot be negative")
	}

	sdkCtx := sdk.UnwrapSDKContext(ctx)
	store := sdkCtx.KVStore(k.storeKey)

	bz, err := amount.Marshal()
	if err != nil {
		return err
	}

	store.Set(addr, bz)
	return nil
}

// Transfer transfers tokens from one account to another
func (k TokenKeeper) Transfer(ctx context.Context, from, to sdk.AccAddress, amount math.Int) error {
	if amount.IsNegative() || amount.IsZero() {
		return sdkerrors.ErrInvalidRequest.Wrap("transfer amount must be positive")
	}

	// Get sender balance
	fromBalance := k.GetBalance(ctx, from)
	if fromBalance.LT(amount) {
		return sdkerrors.ErrInsufficientFunds.Wrapf("insufficient balance: have %s, need %s", fromBalance, amount)
	}

	// Get recipient balance
	toBalance := k.GetBalance(ctx, to)

	// Update balances
	if err := k.SetBalance(ctx, from, fromBalance.Sub(amount)); err != nil {
		return err
	}

	if err := k.SetBalance(ctx, to, toBalance.Add(amount)); err != nil {
		return err
	}

	// Emit transfer event
	sdkCtx := sdk.UnwrapSDKContext(ctx)
	sdkCtx.EventManager().EmitEvent(
		sdk.NewEvent(
			"transfer",
			sdk.NewAttribute("from", from.String()),
			sdk.NewAttribute("to", to.String()),
			sdk.NewAttribute("amount", amount.String()),
		),
	)

	return nil
}

// Mint creates new tokens and adds them to an account
func (k TokenKeeper) Mint(ctx context.Context, addr sdk.AccAddress, amount math.Int) error {
	if amount.IsNegative() || amount.IsZero() {
		return sdkerrors.ErrInvalidRequest.Wrap("mint amount must be positive")
	}

	balance := k.GetBalance(ctx, addr)
	newBalance := balance.Add(amount)

	if err := k.SetBalance(ctx, addr, newBalance); err != nil {
		return err
	}

	// Emit mint event
	sdkCtx := sdk.UnwrapSDKContext(ctx)
	sdkCtx.EventManager().EmitEvent(
		sdk.NewEvent(
			"mint",
			sdk.NewAttribute("recipient", addr.String()),
			sdk.NewAttribute("amount", amount.String()),
		),
	)

	return nil
}

// Burn destroys tokens from an account
func (k TokenKeeper) Burn(ctx context.Context, addr sdk.AccAddress, amount math.Int) error {
	if amount.IsNegative() || amount.IsZero() {
		return sdkerrors.ErrInvalidRequest.Wrap("burn amount must be positive")
	}

	balance := k.GetBalance(ctx, addr)
	if balance.LT(amount) {
		return sdkerrors.ErrInsufficientFunds.Wrapf("insufficient balance: have %s, need %s", balance, amount)
	}

	newBalance := balance.Sub(amount)
	if err := k.SetBalance(ctx, addr, newBalance); err != nil {
		return err
	}

	// Emit burn event
	sdkCtx := sdk.UnwrapSDKContext(ctx)
	sdkCtx.EventManager().EmitEvent(
		sdk.NewEvent(
			"burn",
			sdk.NewAttribute("burner", addr.String()),
			sdk.NewAttribute("amount", amount.String()),
		),
	)

	return nil
}

// GetTotalSupply returns the total supply by iterating all balances
func (k TokenKeeper) GetTotalSupply(ctx context.Context) math.Int {
	sdkCtx := sdk.UnwrapSDKContext(ctx)
	store := sdkCtx.KVStore(k.storeKey)

	totalSupply := math.ZeroInt()
	iterator := store.Iterator(nil, nil)
	defer iterator.Close()

	for ; iterator.Valid(); iterator.Next() {
		var balance math.Int
		if err := balance.Unmarshal(iterator.Value()); err != nil {
			continue
		}
		totalSupply = totalSupply.Add(balance)
	}

	return totalSupply
}

// Example usage and helper functions
type TransferMsg struct {
	From   string `json:"from"`
	To     string `json:"to"`
	Amount string `json:"amount"`
}

type MintMsg struct {
	Recipient string `json:"recipient"`
	Amount    string `json:"amount"`
}

type BurnMsg struct {
	Burner string `json:"burner"`
	Amount string `json:"amount"`
}

// ValidateBasic performs basic validation of transfer message
func (msg TransferMsg) ValidateBasic() error {
	if msg.From == "" {
		return fmt.Errorf("from address cannot be empty")
	}
	if msg.To == "" {
		return fmt.Errorf("to address cannot be empty")
	}
	if msg.Amount == "" {
		return fmt.Errorf("amount cannot be empty")
	}
	return nil
}

// ValidateBasic performs basic validation of mint message
func (msg MintMsg) ValidateBasic() error {
	if msg.Recipient == "" {
		return fmt.Errorf("recipient address cannot be empty")
	}
	if msg.Amount == "" {
		return fmt.Errorf("amount cannot be empty")
	}
	return nil
}

// ValidateBasic performs basic validation of burn message
func (msg BurnMsg) ValidateBasic() error {
	if msg.Burner == "" {
		return fmt.Errorf("burner address cannot be empty")
	}
	if msg.Amount == "" {
		return fmt.Errorf("amount cannot be empty")
	}
	return nil
}
