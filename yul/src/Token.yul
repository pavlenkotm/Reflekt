// Ultra gas-optimized ERC-20 token in Yul
object "Token" {
    code {
        // Constructor code - runs once at deployment
        // Initialize total supply and owner balance
        let totalSupply := 1000000000000000000000000 // 1 million tokens (18 decimals)

        // Store total supply at slot 0
        sstore(0, totalSupply)

        // Store owner balance
        // balances[msg.sender] = totalSupply
        mstore(0, caller())
        mstore(32, 1) // Balances mapping at slot 1
        let ownerBalanceSlot := keccak256(0, 64)
        sstore(ownerBalanceSlot, totalSupply)

        // Deploy runtime code
        datacopy(0, dataoffset("Runtime"), datasize("Runtime"))
        return(0, datasize("Runtime"))
    }

    object "Runtime" {
        code {
            // Function dispatcher
            switch selector()

            // totalSupply() returns (uint256)
            case 0x18160ddd {
                returnUint(sload(0))
            }

            // balanceOf(address) returns (uint256)
            case 0x70a08231 {
                let account := decodeAddress(0)
                returnUint(balanceOf(account))
            }

            // transfer(address,uint256) returns (bool)
            case 0xa9059cbb {
                let to := decodeAddress(0)
                let amount := decodeUint(1)
                let success := transfer(caller(), to, amount)
                returnUint(success)
            }

            // approve(address,uint256) returns (bool)
            case 0x095ea7b3 {
                let spender := decodeAddress(0)
                let amount := decodeUint(1)

                // allowances[msg.sender][spender] = amount
                mstore(0, caller())
                mstore(32, 2) // Allowances mapping at slot 2
                let ownerSlot := keccak256(0, 64)
                mstore(0, spender)
                mstore(32, ownerSlot)
                let allowanceSlot := keccak256(0, 64)
                sstore(allowanceSlot, amount)

                // Emit Approval event
                emitApproval(caller(), spender, amount)
                returnUint(1)
            }

            // allowance(address,address) returns (uint256)
            case 0xdd62ed3e {
                let owner := decodeAddress(0)
                let spender := decodeAddress(1)
                returnUint(allowance(owner, spender))
            }

            // transferFrom(address,address,uint256) returns (bool)
            case 0x23b872dd {
                let from := decodeAddress(0)
                let to := decodeAddress(1)
                let amount := decodeUint(2)

                // Check allowance
                let allowed := allowance(from, caller())
                if lt(allowed, amount) {
                    revertWith("Insufficient allowance")
                }

                // Decrease allowance
                mstore(0, from)
                mstore(32, 2)
                let ownerSlot := keccak256(0, 64)
                mstore(0, caller())
                mstore(32, ownerSlot)
                let allowanceSlot := keccak256(0, 64)
                sstore(allowanceSlot, sub(allowed, amount))

                // Transfer
                let success := transfer(from, to, amount)
                returnUint(success)
            }

            // name() returns (string)
            case 0x06fdde03 {
                returnString("Reflekt Token")
            }

            // symbol() returns (string)
            case 0x95d89b41 {
                returnString("RFLKT")
            }

            // decimals() returns (uint8)
            case 0x313ce567 {
                returnUint(18)
            }

            default {
                revert(0, 0)
            }

            // ========== HELPER FUNCTIONS ==========

            function selector() -> s {
                s := shr(224, calldataload(0))
            }

            function decodeAddress(offset) -> addr {
                addr := shr(96, calldataload(add(4, mul(offset, 32))))
            }

            function decodeUint(offset) -> val {
                val := calldataload(add(4, mul(offset, 32)))
            }

            function balanceOf(account) -> bal {
                mstore(0, account)
                mstore(32, 1) // Balances mapping at slot 1
                let slot := keccak256(0, 64)
                bal := sload(slot)
            }

            function allowance(owner, spender) -> allowed {
                mstore(0, owner)
                mstore(32, 2) // Allowances mapping at slot 2
                let ownerSlot := keccak256(0, 64)
                mstore(0, spender)
                mstore(32, ownerSlot)
                let slot := keccak256(0, 64)
                allowed := sload(slot)
            }

            function transfer(from, to, amount) -> success {
                // Check zero address
                if iszero(to) {
                    revertWith("Transfer to zero address")
                }

                // Get from balance
                let fromBalance := balanceOf(from)

                // Check sufficient balance
                if lt(fromBalance, amount) {
                    revertWith("Insufficient balance")
                }

                // Update from balance
                mstore(0, from)
                mstore(32, 1)
                let fromSlot := keccak256(0, 64)
                sstore(fromSlot, sub(fromBalance, amount))

                // Update to balance
                mstore(0, to)
                mstore(32, 1)
                let toSlot := keccak256(0, 64)
                let toBalance := sload(toSlot)
                sstore(toSlot, add(toBalance, amount))

                // Emit Transfer event
                emitTransfer(from, to, amount)

                success := 1
            }

            function emitTransfer(from, to, amount) {
                // keccak256("Transfer(address,address,uint256)")
                let signature := 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
                mstore(0, amount)
                log3(0, 32, signature, from, to)
            }

            function emitApproval(owner, spender, amount) {
                // keccak256("Approval(address,address,uint256)")
                let signature := 0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925
                mstore(0, amount)
                log3(0, 32, signature, owner, spender)
            }

            function returnUint(val) {
                mstore(0, val)
                return(0, 32)
            }

            function returnString(strLiteral) {
                let len := mload(strLiteral)
                let ptr := 0

                // Offset to string data
                mstore(ptr, 32)
                ptr := add(ptr, 32)

                // String length
                mstore(ptr, len)
                ptr := add(ptr, 32)

                // String data
                for { let i := 0 } lt(i, len) { i := add(i, 32) } {
                    mstore(add(ptr, i), mload(add(strLiteral, add(32, i))))
                }

                return(0, add(64, len))
            }

            function revertWith(message) {
                // Store error message and revert
                let len := mload(message)
                mstore(0, message)
                revert(0, len)
            }
        }
    }

    // String literals
    data "name" hex"0000000000000000000000000000000000000000000000000000000000000020" // offset
              hex"000000000000000000000000000000000000000000000000000000000000000e" // length = 14
              hex"5265666c656b7420546f6b656e0000000000000000000000000000000000000" // "Reflekt Token"

    data "symbol" hex"0000000000000000000000000000000000000000000000000000000000000020" // offset
                hex"0000000000000000000000000000000000000000000000000000000000000005" // length = 5
                hex"52464c4b540000000000000000000000000000000000000000000000000000000" // "RFLKT"
}
