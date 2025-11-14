#![cfg_attr(not(feature = "std"), no_std, no_main)]

#[ink::contract]
mod erc20 {
    use ink::storage::Mapping;

    /// Event emitted when tokens are transferred
    #[ink(event)]
    pub struct Transfer {
        #[ink(topic)]
        from: Option<AccountId>,
        #[ink(topic)]
        to: Option<AccountId>,
        value: Balance,
    }

    /// Event emitted when an approval is made
    #[ink(event)]
    pub struct Approval {
        #[ink(topic)]
        owner: AccountId,
        #[ink(topic)]
        spender: AccountId,
        value: Balance,
    }

    /// The ERC-20 error types
    #[derive(Debug, PartialEq, Eq)]
    #[ink::scale_derive(Encode, Decode, TypeInfo)]
    pub enum Error {
        /// Insufficient balance for transfer
        InsufficientBalance,
        /// Insufficient allowance for transfer
        InsufficientAllowance,
    }

    /// The ERC-20 result type
    pub type Result<T> = core::result::Result<T, Error>;

    /// ERC-20 token contract storage
    #[ink(storage)]
    pub struct Erc20 {
        /// Total token supply
        total_supply: Balance,
        /// Mapping from account to token balance
        balances: Mapping<AccountId, Balance>,
        /// Mapping from (owner, spender) to allowance
        allowances: Mapping<(AccountId, AccountId), Balance>,
    }

    impl Erc20 {
        /// Constructor that initializes the total supply and assigns it to the caller
        #[ink(constructor)]
        pub fn new(total_supply: Balance) -> Self {
            let mut balances = Mapping::default();
            let caller = Self::env().caller();
            balances.insert(caller, &total_supply);

            Self::env().emit_event(Transfer {
                from: None,
                to: Some(caller),
                value: total_supply,
            });

            Self {
                total_supply,
                balances,
                allowances: Default::default(),
            }
        }

        /// Returns the total token supply
        #[ink(message)]
        pub fn total_supply(&self) -> Balance {
            self.total_supply
        }

        /// Returns the account balance for the specified `owner`
        #[ink(message)]
        pub fn balance_of(&self, owner: AccountId) -> Balance {
            self.balances.get(owner).unwrap_or(0)
        }

        /// Returns the allowance for `spender` approved by `owner`
        #[ink(message)]
        pub fn allowance(&self, owner: AccountId, spender: AccountId) -> Balance {
            self.allowances.get((owner, spender)).unwrap_or(0)
        }

        /// Transfers `value` amount of tokens from the caller to `to`
        #[ink(message)]
        pub fn transfer(&mut self, to: AccountId, value: Balance) -> Result<()> {
            let from = self.env().caller();
            self.transfer_from_to(&from, &to, value)
        }

        /// Approves `spender` to spend `value` amount of tokens on behalf of caller
        #[ink(message)]
        pub fn approve(&mut self, spender: AccountId, value: Balance) -> Result<()> {
            let owner = self.env().caller();
            self.allowances.insert((owner, spender), &value);

            self.env().emit_event(Approval {
                owner,
                spender,
                value,
            });

            Ok(())
        }

        /// Transfers `value` tokens from `from` to `to` on behalf of `from`
        #[ink(message)]
        pub fn transfer_from(
            &mut self,
            from: AccountId,
            to: AccountId,
            value: Balance,
        ) -> Result<()> {
            let caller = self.env().caller();
            let allowance = self.allowance(from, caller);

            if allowance < value {
                return Err(Error::InsufficientAllowance);
            }

            self.transfer_from_to(&from, &to, value)?;
            self.allowances.insert((from, caller), &(allowance - value));

            Ok(())
        }

        /// Helper function to transfer tokens between accounts
        fn transfer_from_to(
            &mut self,
            from: &AccountId,
            to: &AccountId,
            value: Balance,
        ) -> Result<()> {
            let from_balance = self.balance_of(*from);

            if from_balance < value {
                return Err(Error::InsufficientBalance);
            }

            self.balances.insert(from, &(from_balance - value));
            let to_balance = self.balance_of(*to);
            self.balances.insert(to, &(to_balance + value));

            self.env().emit_event(Transfer {
                from: Some(*from),
                to: Some(*to),
                value,
            });

            Ok(())
        }

        /// Mints new tokens (only for demonstration - in production, add access control)
        #[ink(message)]
        pub fn mint(&mut self, to: AccountId, value: Balance) -> Result<()> {
            let to_balance = self.balance_of(to);
            self.balances.insert(to, &(to_balance + value));
            self.total_supply += value;

            self.env().emit_event(Transfer {
                from: None,
                to: Some(to),
                value,
            });

            Ok(())
        }

        /// Burns tokens from caller's account
        #[ink(message)]
        pub fn burn(&mut self, value: Balance) -> Result<()> {
            let caller = self.env().caller();
            let caller_balance = self.balance_of(caller);

            if caller_balance < value {
                return Err(Error::InsufficientBalance);
            }

            self.balances.insert(caller, &(caller_balance - value));
            self.total_supply -= value;

            self.env().emit_event(Transfer {
                from: Some(caller),
                to: None,
                value,
            });

            Ok(())
        }
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[ink::test]
        fn new_works() {
            let erc20 = Erc20::new(1000);
            assert_eq!(erc20.total_supply(), 1000);
        }

        #[ink::test]
        fn balance_works() {
            let erc20 = Erc20::new(1000);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();
            assert_eq!(erc20.balance_of(accounts.alice), 1000);
            assert_eq!(erc20.balance_of(accounts.bob), 0);
        }

        #[ink::test]
        fn transfer_works() {
            let mut erc20 = Erc20::new(1000);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            assert_eq!(erc20.balance_of(accounts.alice), 1000);
            assert!(erc20.transfer(accounts.bob, 100).is_ok());
            assert_eq!(erc20.balance_of(accounts.alice), 900);
            assert_eq!(erc20.balance_of(accounts.bob), 100);
        }

        #[ink::test]
        fn transfer_fails_with_insufficient_balance() {
            let mut erc20 = Erc20::new(100);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            let result = erc20.transfer(accounts.bob, 200);
            assert_eq!(result, Err(Error::InsufficientBalance));
        }

        #[ink::test]
        fn approve_works() {
            let mut erc20 = Erc20::new(1000);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            assert!(erc20.approve(accounts.bob, 200).is_ok());
            assert_eq!(erc20.allowance(accounts.alice, accounts.bob), 200);
        }

        #[ink::test]
        fn transfer_from_works() {
            let mut erc20 = Erc20::new(1000);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            assert!(erc20.approve(accounts.bob, 200).is_ok());

            // Set caller to bob
            ink::env::test::set_caller::<ink::env::DefaultEnvironment>(accounts.bob);
            assert!(erc20.transfer_from(accounts.alice, accounts.charlie, 100).is_ok());

            assert_eq!(erc20.balance_of(accounts.alice), 900);
            assert_eq!(erc20.balance_of(accounts.charlie), 100);
            assert_eq!(erc20.allowance(accounts.alice, accounts.bob), 100);
        }

        #[ink::test]
        fn burn_works() {
            let mut erc20 = Erc20::new(1000);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            assert!(erc20.burn(100).is_ok());
            assert_eq!(erc20.balance_of(accounts.alice), 900);
            assert_eq!(erc20.total_supply(), 900);
        }

        #[ink::test]
        fn mint_works() {
            let mut erc20 = Erc20::new(1000);
            let accounts = ink::env::test::default_accounts::<ink::env::DefaultEnvironment>();

            assert!(erc20.mint(accounts.bob, 500).is_ok());
            assert_eq!(erc20.balance_of(accounts.bob), 500);
            assert_eq!(erc20.total_supply(), 1500);
        }
    }

    #[cfg(all(test, feature = "e2e-tests"))]
    mod e2e_tests {
        use super::*;
        use ink_e2e::ContractsBackend;

        type E2EResult<T> = std::result::Result<T, Box<dyn std::error::Error>>;

        #[ink_e2e::test]
        async fn e2e_transfer_works<Client: E2EBackend>(mut client: Client) -> E2EResult<()> {
            // Deploy contract
            let total_supply = 1_000_000;
            let constructor = Erc20Ref::new(total_supply);
            let contract = client
                .instantiate("erc20", &ink_e2e::alice(), constructor)
                .submit()
                .await
                .expect("instantiate failed");
            let call_result = contract.call_result();

            // Transfer tokens
            let transfer_to = ink_e2e::bob();
            let transfer_amount = 1000;

            let transfer = contract.call::<Erc20>().transfer(transfer_to.clone(), transfer_amount);
            let transfer_result = client
                .call(&ink_e2e::alice(), &transfer)
                .submit()
                .await
                .expect("transfer failed");

            assert!(transfer_result.return_value().is_ok());

            Ok(())
        }
    }
}
