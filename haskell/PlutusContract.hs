{-# LANGUAGE DataKinds #-}
{-# LANGUAGE TemplateHaskell #-}
{-# LANGUAGE TypeApplications #-}
{-# LANGUAGE OverloadedStrings #-}

module PlutusContract where

import qualified PlutusTx
import PlutusTx.Prelude
import qualified Plutus.V2.Ledger.Api as PlutusV2
import qualified Ledger
import qualified Ledger.Typed.Scripts as Scripts

{-|
  Simple Plutus Smart Contract for Cardano
  Demonstrates Haskell's type-safe approach to smart contracts
-}

-- | Contract parameters
data ContractParams = ContractParams
    { beneficiary :: PlutusV2.PubKeyHash
    , deadline    :: PlutusV2.POSIXTime
    }

PlutusTx.makeLift ''ContractParams

-- | Contract datum (state stored on-chain)
data ContractDatum = ContractDatum
    { amount :: Integer
    , owner  :: PlutusV2.PubKeyHash
    }

PlutusTx.unstableMakeIsData ''ContractDatum

-- | Validator redeemer (action to perform)
data ContractRedeemer = Release | Refund

PlutusTx.unstableMakeIsData ''ContractRedeemer

-- | Main validator logic
{-# INLINABLE mkValidator #-}
mkValidator :: ContractParams -> ContractDatum -> ContractRedeemer -> PlutusV2.ScriptContext -> Bool
mkValidator params datum redeemer ctx =
    case redeemer of
        Release ->
            -- Check if beneficiary is signing and deadline has passed
            traceIfFalse "Beneficiary must sign" signedByBeneficiary &&
            traceIfFalse "Deadline not reached" deadlinePassed

        Refund ->
            -- Check if owner is signing
            traceIfFalse "Owner must sign" signedByOwner
  where
    info :: PlutusV2.TxInfo
    info = PlutusV2.scriptContextTxInfo ctx

    signedByBeneficiary :: Bool
    signedByBeneficiary =
        PlutusV2.txSignedBy info (beneficiary params)

    signedByOwner :: Bool
    signedByOwner =
        PlutusV2.txSignedBy info (owner datum)

    deadlinePassed :: Bool
    deadlinePassed =
        PlutusV2.from (deadline params) `PlutusV2.contains` PlutusV2.txInfoValidRange info

-- | Compile validator
validator :: ContractParams -> Scripts.TypedValidator ContractType
validator params = Scripts.mkTypedValidator @ContractType
    ($$(PlutusTx.compile [|| mkValidator ||]) `PlutusTx.applyCode` PlutusTx.liftCode params)
    $$(PlutusTx.compile [|| wrap ||])
  where
    wrap = Scripts.wrapValidator @ContractDatum @ContractRedeemer

-- | Contract type definition
data ContractType
instance Scripts.ValidatorTypes ContractType where
    type instance DatumType ContractType = ContractDatum
    type instance RedeemerType ContractType = ContractRedeemer

-- | Get validator script
validatorScript :: ContractParams -> Ledger.Validator
validatorScript = Scripts.validatorScript . validator

-- | Get validator address
validatorAddress :: ContractParams -> Ledger.Address
validatorAddress = Ledger.scriptAddress . validatorScript

-- Example usage
exampleParams :: ContractParams
exampleParams = ContractParams
    { beneficiary = "abc123..."  -- Example public key hash
    , deadline = 1700000000000   -- Example POSIX timestamp
    }
