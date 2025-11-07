use anchor_lang::prelude::*;

declare_id!("11111111111111111111111111111111");

#[program]
pub mod counter_program {
    use super::*;

    /// Initialize a new counter account
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = 0;
        counter.authority = ctx.accounts.authority.key();
        msg!("Counter initialized with value: {}", counter.count);
        Ok(())
    }

    /// Increment the counter by a specified amount
    pub fn increment(ctx: Context<Update>, amount: u64) -> Result<()> {
        let counter = &mut ctx.accounts.counter;

        require!(
            amount > 0,
            CounterError::InvalidAmount
        );

        counter.count = counter
            .count
            .checked_add(amount)
            .ok_or(CounterError::Overflow)?;

        msg!("Counter incremented to: {}", counter.count);
        Ok(())
    }

    /// Decrement the counter by a specified amount
    pub fn decrement(ctx: Context<Update>, amount: u64) -> Result<()> {
        let counter = &mut ctx.accounts.counter;

        require!(
            amount > 0,
            CounterError::InvalidAmount
        );

        counter.count = counter
            .count
            .checked_sub(amount)
            .ok_or(CounterError::Underflow)?;

        msg!("Counter decremented to: {}", counter.count);
        Ok(())
    }

    /// Reset the counter to zero
    pub fn reset(ctx: Context<Update>) -> Result<()> {
        let counter = &mut ctx.accounts.counter;
        counter.count = 0;
        msg!("Counter reset to: {}", counter.count);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + Counter::INIT_SPACE
    )]
    pub counter: Account<'info, Counter>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Update<'info> {
    #[account(
        mut,
        has_one = authority @ CounterError::Unauthorized
    )]
    pub counter: Account<'info, Counter>,

    pub authority: Signer<'info>,
}

#[account]
#[derive(InitSpace)]
pub struct Counter {
    pub count: u64,
    pub authority: Pubkey,
}

#[error_code]
pub enum CounterError {
    #[msg("The provided amount must be greater than zero")]
    InvalidAmount,

    #[msg("Arithmetic overflow occurred")]
    Overflow,

    #[msg("Arithmetic underflow occurred")]
    Underflow,

    #[msg("Unauthorized: Only the authority can perform this action")]
    Unauthorized,
}
