# @version ^0.3.9
"""
@title SimpleVault
@notice A simple ETH vault contract demonstrating Vyper syntax
@dev Allows users to deposit and withdraw ETH with basic access control
@author Reflekt
"""

# Events
event Deposit:
    user: indexed(address)
    amount: uint256
    timestamp: uint256

event Withdrawal:
    user: indexed(address)
    amount: uint256
    timestamp: uint256

event OwnershipTransferred:
    previous_owner: indexed(address)
    new_owner: indexed(address)

# State variables
owner: public(address)
balances: public(HashMap[address, uint256])
total_deposited: public(uint256)
is_paused: public(bool)

@external
def __init__():
    """
    @notice Contract constructor
    @dev Sets the deployer as the initial owner
    """
    self.owner = msg.sender
    self.is_paused = False

@external
@payable
def deposit():
    """
    @notice Deposit ETH into the vault
    @dev Increases the user's balance and emits a Deposit event
    """
    assert not self.is_paused, "Contract is paused"
    assert msg.value > 0, "Must send ETH"

    self.balances[msg.sender] += msg.value
    self.total_deposited += msg.value

    log Deposit(msg.sender, msg.value, block.timestamp)

@external
def withdraw(amount: uint256):
    """
    @notice Withdraw ETH from the vault
    @dev Decreases the user's balance and sends ETH
    @param amount Amount of ETH to withdraw (in wei)
    """
    assert not self.is_paused, "Contract is paused"
    assert amount > 0, "Amount must be positive"
    assert self.balances[msg.sender] >= amount, "Insufficient balance"

    self.balances[msg.sender] -= amount

    send(msg.sender, amount)

    log Withdrawal(msg.sender, amount, block.timestamp)

@external
def withdraw_all():
    """
    @notice Withdraw all deposited ETH
    @dev Convenience function to withdraw entire balance
    """
    amount: uint256 = self.balances[msg.sender]
    assert amount > 0, "No balance to withdraw"

    self.withdraw(amount)

@external
def pause():
    """
    @notice Pause contract operations
    @dev Only owner can pause
    """
    assert msg.sender == self.owner, "Only owner"
    self.is_paused = True

@external
def unpause():
    """
    @notice Unpause contract operations
    @dev Only owner can unpause
    """
    assert msg.sender == self.owner, "Only owner"
    self.is_paused = False

@external
def transfer_ownership(new_owner: address):
    """
    @notice Transfer ownership to a new address
    @dev Only current owner can transfer ownership
    @param new_owner Address of the new owner
    """
    assert msg.sender == self.owner, "Only owner"
    assert new_owner != empty(address), "Invalid address"

    old_owner: address = self.owner
    self.owner = new_owner

    log OwnershipTransferred(old_owner, new_owner)

@external
@view
def get_balance(user: address) -> uint256:
    """
    @notice Get the balance of a user
    @param user Address of the user
    @return Balance in wei
    """
    return self.balances[user]

@external
@view
def get_contract_balance() -> uint256:
    """
    @notice Get the total ETH balance of the contract
    @return Contract balance in wei
    """
    return self.balance
