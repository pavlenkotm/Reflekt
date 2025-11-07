module reflekt::token_swap {
    use std::signer;
    use aptos_framework::coin::{Self, Coin};
    use aptos_framework::account;

    /// Error codes
    const E_NOT_INITIALIZED: u64 = 1;
    const E_ALREADY_INITIALIZED: u64 = 2;
    const E_INSUFFICIENT_LIQUIDITY: u64 = 3;
    const E_INVALID_AMOUNT: u64 = 4;
    const E_SLIPPAGE_EXCEEDED: u64 = 5;

    /// Liquidity pool structure
    struct LiquidityPool<phantom CoinX, phantom CoinY> has key {
        coin_x_reserve: Coin<CoinX>,
        coin_y_reserve: Coin<CoinY>,
        lp_token_supply: u64,
    }

    /// LP token capability
    struct LPTokenCapability has key, store {
        mint_cap: coin::MintCapability<LPToken>,
        burn_cap: coin::BurnCapability<LPToken>,
    }

    /// LP token marker
    struct LPToken {}

    /// Initialize the liquidity pool
    public entry fun initialize_pool<CoinX, CoinY>(
        admin: &signer,
    ) acquires LiquidityPool {
        let admin_addr = signer::address_of(admin);

        assert!(
            !exists<LiquidityPool<CoinX, CoinY>>(admin_addr),
            E_ALREADY_INITIALIZED
        );

        let coin_x_reserve = coin::zero<CoinX>();
        let coin_y_reserve = coin::zero<CoinY>();

        move_to(admin, LiquidityPool<CoinX, CoinY> {
            coin_x_reserve,
            coin_y_reserve,
            lp_token_supply: 0,
        });
    }

    /// Add liquidity to the pool
    public entry fun add_liquidity<CoinX, CoinY>(
        provider: &signer,
        amount_x: u64,
        amount_y: u64,
        pool_addr: address,
    ) acquires LiquidityPool {
        assert!(amount_x > 0 && amount_y > 0, E_INVALID_AMOUNT);
        assert!(exists<LiquidityPool<CoinX, CoinY>>(pool_addr), E_NOT_INITIALIZED);

        let pool = borrow_global_mut<LiquidityPool<CoinX, CoinY>>(pool_addr);

        // Withdraw coins from provider
        let coin_x = coin::withdraw<CoinX>(provider, amount_x);
        let coin_y = coin::withdraw<CoinY>(provider, amount_y);

        // Merge coins into pool reserves
        coin::merge(&mut pool.coin_x_reserve, coin_x);
        coin::merge(&mut pool.coin_y_reserve, coin_y);

        // Calculate LP tokens to mint (simplified)
        let lp_tokens = if (pool.lp_token_supply == 0) {
            // First liquidity provider gets sqrt(x * y)
            integer_sqrt(amount_x * amount_y)
        } else {
            // Subsequent providers get proportional tokens
            (amount_x * pool.lp_token_supply) / coin::value(&pool.coin_x_reserve)
        };

        pool.lp_token_supply = pool.lp_token_supply + lp_tokens;
    }

    /// Swap CoinX for CoinY
    public entry fun swap_x_to_y<CoinX, CoinY>(
        trader: &signer,
        amount_in: u64,
        min_amount_out: u64,
        pool_addr: address,
    ) acquires LiquidityPool {
        assert!(amount_in > 0, E_INVALID_AMOUNT);
        assert!(exists<LiquidityPool<CoinX, CoinY>>(pool_addr), E_NOT_INITIALIZED);

        let pool = borrow_global_mut<LiquidityPool<CoinX, CoinY>>(pool_addr);

        // Calculate output amount using constant product formula: x * y = k
        let reserve_x = coin::value(&pool.coin_x_reserve);
        let reserve_y = coin::value(&pool.coin_y_reserve);

        let amount_out = calculate_output_amount(amount_in, reserve_x, reserve_y);

        assert!(amount_out >= min_amount_out, E_SLIPPAGE_EXCEEDED);
        assert!(amount_out <= reserve_y, E_INSUFFICIENT_LIQUIDITY);

        // Withdraw input coins from trader
        let coin_in = coin::withdraw<CoinX>(trader, amount_in);

        // Extract output coins from pool
        let coin_out = coin::extract(&mut pool.coin_y_reserve, amount_out);

        // Merge input coins to pool
        coin::merge(&mut pool.coin_x_reserve, coin_in);

        // Deposit output coins to trader
        coin::deposit(signer::address_of(trader), coin_out);
    }

    /// Swap CoinY for CoinX
    public entry fun swap_y_to_x<CoinX, CoinY>(
        trader: &signer,
        amount_in: u64,
        min_amount_out: u64,
        pool_addr: address,
    ) acquires LiquidityPool {
        assert!(amount_in > 0, E_INVALID_AMOUNT);
        assert!(exists<LiquidityPool<CoinX, CoinY>>(pool_addr), E_NOT_INITIALIZED);

        let pool = borrow_global_mut<LiquidityPool<CoinX, CoinY>>(pool_addr);

        let reserve_x = coin::value(&pool.coin_x_reserve);
        let reserve_y = coin::value(&pool.coin_y_reserve);

        let amount_out = calculate_output_amount(amount_in, reserve_y, reserve_x);

        assert!(amount_out >= min_amount_out, E_SLIPPAGE_EXCEEDED);
        assert!(amount_out <= reserve_x, E_INSUFFICIENT_LIQUIDITY);

        let coin_in = coin::withdraw<CoinY>(trader, amount_in);
        let coin_out = coin::extract(&mut pool.coin_x_reserve, amount_out);

        coin::merge(&mut pool.coin_y_reserve, coin_in);
        coin::deposit(signer::address_of(trader), coin_out);
    }

    /// Calculate output amount for swap (with 0.3% fee)
    fun calculate_output_amount(
        amount_in: u64,
        reserve_in: u64,
        reserve_out: u64,
    ): u64 {
        let amount_in_with_fee = amount_in * 997; // 0.3% fee
        let numerator = amount_in_with_fee * reserve_out;
        let denominator = (reserve_in * 1000) + amount_in_with_fee;
        numerator / denominator
    }

    /// Helper function to calculate integer square root
    fun integer_sqrt(x: u64): u64 {
        if (x == 0) return 0;

        let z = x;
        let y = (x + 1) / 2;

        while (y < z) {
            z = y;
            y = (x / y + y) / 2;
        };

        z
    }

    /// Get pool reserves
    #[view]
    public fun get_reserves<CoinX, CoinY>(pool_addr: address): (u64, u64) acquires LiquidityPool {
        assert!(exists<LiquidityPool<CoinX, CoinY>>(pool_addr), E_NOT_INITIALIZED);
        let pool = borrow_global<LiquidityPool<CoinX, CoinY>>(pool_addr);
        (coin::value(&pool.coin_x_reserve), coin::value(&pool.coin_y_reserve))
    }

    #[test_only]
    use aptos_framework::managed_coin;

    #[test(admin = @reflekt)]
    fun test_initialize_pool(admin: &signer) acquires LiquidityPool {
        // Test initialization
        initialize_pool<LPToken, LPToken>(admin);
        assert!(exists<LiquidityPool<LPToken, LPToken>>(signer::address_of(admin)), 0);
    }
}
