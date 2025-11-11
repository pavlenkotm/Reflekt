contract;

use std::{
    asset::{
        mint_to,
        burn,
        transfer,
    },
    call_frames::msg_asset_id,
    context::{
        msg_amount,
        this_balance,
    },
    hash::Hash,
    storage::storage_string::*,
};

storage {
    /// Total supply of the token
    total_supply: u64 = 0,
    /// Token name
    name: StorageString = StorageString {},
    /// Token symbol
    symbol: StorageString = StorageString {},
    /// Balances mapping
    balances: StorageMap<Identity, u64> = StorageMap {},
    /// Allowances for spending
    allowances: StorageMap<(Identity, Identity), u64> = StorageMap {},
    /// Owner of the contract
    owner: Option<Identity> = Option::None,
}

abi Token {
    /// Initialize the token
    #[storage(read, write)]
    fn constructor(name: str[10], symbol: str[5], initial_supply: u64, owner: Identity);

    /// Get token name
    #[storage(read)]
    fn name() -> str[10];

    /// Get token symbol
    #[storage(read)]
    fn symbol() -> str[5];

    /// Get total supply
    #[storage(read)]
    fn total_supply() -> u64;

    /// Get balance of an account
    #[storage(read)]
    fn balance_of(account: Identity) -> u64;

    /// Mint new tokens (owner only)
    #[storage(read, write)]
    fn mint(recipient: Identity, amount: u64);

    /// Burn tokens
    #[storage(read, write)]
    fn burn(amount: u64);

    /// Transfer tokens
    #[storage(read, write)]
    fn transfer(recipient: Identity, amount: u64) -> bool;

    /// Approve spending
    #[storage(read, write)]
    fn approve(spender: Identity, amount: u64) -> bool;

    /// Get allowance
    #[storage(read)]
    fn allowance(owner: Identity, spender: Identity) -> u64;

    /// Transfer from approved account
    #[storage(read, write)]
    fn transfer_from(sender: Identity, recipient: Identity, amount: u64) -> bool;
}

impl Token for Contract {
    #[storage(read, write)]
    fn constructor(name: str[10], symbol: str[5], initial_supply: u64, owner: Identity) {
        // Set token metadata
        storage.name.write_slice(name);
        storage.symbol.write_slice(symbol);
        storage.owner.write(Option::Some(owner));

        // Mint initial supply to owner
        storage.total_supply.write(initial_supply);
        storage.balances.insert(owner, initial_supply);
    }

    #[storage(read)]
    fn name() -> str[10] {
        storage.name.read_slice().unwrap()
    }

    #[storage(read)]
    fn symbol() -> str[5] {
        storage.symbol.read_slice().unwrap()
    }

    #[storage(read)]
    fn total_supply() -> u64 {
        storage.total_supply.read()
    }

    #[storage(read)]
    fn balance_of(account: Identity) -> u64 {
        storage.balances.get(account).try_read().unwrap_or(0)
    }

    #[storage(read, write)]
    fn mint(recipient: Identity, amount: u64) {
        // Only owner can mint
        let caller = msg_sender().unwrap();
        let owner = storage.owner.read().unwrap();
        require(caller == owner, "Only owner can mint");

        // Update total supply
        let current_supply = storage.total_supply.read();
        storage.total_supply.write(current_supply + amount);

        // Update recipient balance
        let current_balance = storage.balances.get(recipient).try_read().unwrap_or(0);
        storage.balances.insert(recipient, current_balance + amount);

        // Mint native asset
        mint_to(recipient, amount);
    }

    #[storage(read, write)]
    fn burn(amount: u64) {
        let caller = msg_sender().unwrap();

        // Check balance
        let current_balance = storage.balances.get(caller).try_read().unwrap_or(0);
        require(current_balance >= amount, "Insufficient balance");

        // Update balance and supply
        storage.balances.insert(caller, current_balance - amount);
        let current_supply = storage.total_supply.read();
        storage.total_supply.write(current_supply - amount);

        // Burn native asset
        burn(amount);
    }

    #[storage(read, write)]
    fn transfer(recipient: Identity, amount: u64) -> bool {
        let sender = msg_sender().unwrap();

        // Check balance
        let sender_balance = storage.balances.get(sender).try_read().unwrap_or(0);
        require(sender_balance >= amount, "Insufficient balance");

        // Update balances
        storage.balances.insert(sender, sender_balance - amount);
        let recipient_balance = storage.balances.get(recipient).try_read().unwrap_or(0);
        storage.balances.insert(recipient, recipient_balance + amount);

        // Transfer native asset
        transfer(recipient, msg_asset_id(), amount);

        true
    }

    #[storage(read, write)]
    fn approve(spender: Identity, amount: u64) -> bool {
        let owner = msg_sender().unwrap();
        storage.allowances.insert((owner, spender), amount);
        true
    }

    #[storage(read)]
    fn allowance(owner: Identity, spender: Identity) -> u64 {
        storage.allowances.get((owner, spender)).try_read().unwrap_or(0)
    }

    #[storage(read, write)]
    fn transfer_from(sender: Identity, recipient: Identity, amount: u64) -> bool {
        let caller = msg_sender().unwrap();

        // Check allowance
        let current_allowance = storage.allowances.get((sender, caller)).try_read().unwrap_or(0);
        require(current_allowance >= amount, "Insufficient allowance");

        // Check sender balance
        let sender_balance = storage.balances.get(sender).try_read().unwrap_or(0);
        require(sender_balance >= amount, "Insufficient balance");

        // Update allowance
        storage.allowances.insert((sender, caller), current_allowance - amount);

        // Update balances
        storage.balances.insert(sender, sender_balance - amount);
        let recipient_balance = storage.balances.get(recipient).try_read().unwrap_or(0);
        storage.balances.insert(recipient, recipient_balance + amount);

        true
    }
}
