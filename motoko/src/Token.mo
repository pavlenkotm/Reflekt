import Principal "mo:base/Principal";
import HashMap "mo:base/HashMap";
import Iter "mo:base/Iter";
import Array "mo:base/Array";
import Option "mo:base/Option";
import Result "mo:base/Result";
import Nat "mo:base/Nat";
import Time "mo:base/Time";

actor Token {
    // Types
    public type Account = Principal;
    public type Amount = Nat;
    public type TxIndex = Nat;

    public type TransferArgs = {
        to: Account;
        amount: Amount;
        memo: ?Blob;
    };

    public type TransferError = {
        #InsufficientBalance;
        #InvalidReceiver;
    };

    public type Metadata = {
        name: Text;
        symbol: Text;
        decimals: Nat8;
        totalSupply: Nat;
        owner: Principal;
    };

    public type Transaction = {
        from: Account;
        to: Account;
        amount: Amount;
        timestamp: Time.Time;
    };

    // State
    private stable var name_ : Text = "Reflekt Token";
    private stable var symbol_ : Text = "RFLKT";
    private stable var decimals_ : Nat8 = 8;
    private stable var totalSupply_ : Nat = 1_000_000_00000000;
    private stable var owner_ : Principal = Principal.fromText("aaaaa-aa");

    // Non-stable state (must use upgrade hooks)
    private var balances = HashMap.HashMap<Account, Amount>(10, Principal.equal, Principal.hash);
    private var allowances = HashMap.HashMap<Account, HashMap.HashMap<Account, Amount>>(
        10,
        Principal.equal,
        Principal.hash
    );
    private var transactions : [Transaction] = [];

    // Stable arrays for upgrades
    private stable var stableBalances : [(Account, Amount)] = [];
    private stable var stableAllowances : [(Account, [(Account, Amount)])] = [];
    private stable var stableTransactions : [Transaction] = [];

    // Initialization
    system func preupgrade() {
        stableBalances := Iter.toArray(balances.entries());

        let allowanceEntries = Iter.toArray(allowances.entries());
        stableAllowances := Array.map<(Account, HashMap.HashMap<Account, Amount>), (Account, [(Account, Amount)])>(
            allowanceEntries,
            func(entry) {
                let (account, accountAllowances) = entry;
                (account, Iter.toArray(accountAllowances.entries()))
            }
        );

        stableTransactions := transactions;
    };

    system func postupgrade() {
        balances := HashMap.fromIter<Account, Amount>(
            stableBalances.vals(),
            10,
            Principal.equal,
            Principal.hash
        );

        allowances := HashMap.HashMap<Account, HashMap.HashMap<Account, Amount>>(
            10,
            Principal.equal,
            Principal.hash
        );

        for ((account, accountAllowances) in stableAllowances.vals()) {
            let innerMap = HashMap.fromIter<Account, Amount>(
                accountAllowances.vals(),
                10,
                Principal.equal,
                Principal.hash
            );
            allowances.put(account, innerMap);
        };

        transactions := stableTransactions;

        // Clear stable arrays to save space
        stableBalances := [];
        stableAllowances := [];
    };

    // Initialize with owner balance
    private func init() {
        balances.put(owner_, totalSupply_);
    };

    // Public query methods (read-only, fast, free)
    public query func name() : async Text {
        name_
    };

    public query func symbol() : async Text {
        symbol_
    };

    public query func decimals() : async Nat8 {
        decimals_
    };

    public query func totalSupply() : async Nat {
        totalSupply_
    };

    public query func balanceOf(account: Account) : async Nat {
        Option.get(balances.get(account), 0)
    };

    public query func allowance(owner: Account, spender: Account) : async Nat {
        switch (allowances.get(owner)) {
            case null { 0 };
            case (?ownerAllowances) {
                Option.get(ownerAllowances.get(spender), 0)
            };
        }
    };

    public query func metadata() : async Metadata {
        {
            name = name_;
            symbol = symbol_;
            decimals = decimals_;
            totalSupply = totalSupply_;
            owner = owner_;
        }
    };

    public query func getTransactions() : async [Transaction] {
        transactions
    };

    // Public update methods (modify state, go through consensus)
    public shared(msg) func transfer(to: Account, amount: Amount) : async Result.Result<TxIndex, TransferError> {
        if (Principal.isAnonymous(to)) {
            return #err(#InvalidReceiver);
        };

        let from = msg.caller;
        let fromBalance = Option.get(balances.get(from), 0);

        if (fromBalance < amount) {
            return #err(#InsufficientBalance);
        };

        // Update balances
        balances.put(from, fromBalance - amount);
        let toBalance = Option.get(balances.get(to), 0);
        balances.put(to, toBalance + amount);

        // Record transaction
        let tx : Transaction = {
            from = from;
            to = to;
            amount = amount;
            timestamp = Time.now();
        };
        transactions := Array.append(transactions, [tx]);

        #ok(transactions.size() - 1)
    };

    public shared(msg) func approve(spender: Account, amount: Amount) : async Bool {
        let owner = msg.caller;

        switch (allowances.get(owner)) {
            case null {
                let newMap = HashMap.HashMap<Account, Amount>(1, Principal.equal, Principal.hash);
                newMap.put(spender, amount);
                allowances.put(owner, newMap);
            };
            case (?ownerAllowances) {
                ownerAllowances.put(spender, amount);
            };
        };

        true
    };

    public shared(msg) func transferFrom(
        from: Account,
        to: Account,
        amount: Amount
    ) : async Result.Result<TxIndex, TransferError> {
        if (Principal.isAnonymous(to)) {
            return #err(#InvalidReceiver);
        };

        let spender = msg.caller;

        // Check allowance
        let allowance = switch (allowances.get(from)) {
            case null { 0 };
            case (?ownerAllowances) {
                Option.get(ownerAllowances.get(spender), 0)
            };
        };

        if (allowance < amount) {
            return #err(#InsufficientBalance);
        };

        // Check balance
        let fromBalance = Option.get(balances.get(from), 0);
        if (fromBalance < amount) {
            return #err(#InsufficientBalance);
        };

        // Update allowance
        switch (allowances.get(from)) {
            case (?ownerAllowances) {
                ownerAllowances.put(spender, allowance - amount);
            };
            case null { };
        };

        // Update balances
        balances.put(from, fromBalance - amount);
        let toBalance = Option.get(balances.get(to), 0);
        balances.put(to, toBalance + amount);

        // Record transaction
        let tx : Transaction = {
            from = from;
            to = to;
            amount = amount;
            timestamp = Time.now();
        };
        transactions := Array.append(transactions, [tx]);

        #ok(transactions.size() - 1)
    };

    // Owner-only functions
    public shared(msg) func mint(to: Account, amount: Amount) : async Result.Result<(), Text> {
        if (msg.caller != owner_) {
            return #err("Only owner can mint");
        };

        if (Principal.isAnonymous(to)) {
            return #err("Invalid receiver");
        };

        totalSupply_ += amount;
        let toBalance = Option.get(balances.get(to), 0);
        balances.put(to, toBalance + amount);

        #ok()
    };

    public shared(msg) func burn(amount: Amount) : async Result.Result<(), Text> {
        let from = msg.caller;
        let fromBalance = Option.get(balances.get(from), 0);

        if (fromBalance < amount) {
            return #err("Insufficient balance");
        };

        balances.put(from, fromBalance - amount);
        totalSupply_ -= amount;

        #ok()
    };

    // Initialize on first deploy
    init();
}
