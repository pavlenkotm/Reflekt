;; SIP-010 Fungible Token Implementation
;; Reflekt Token - A standard fungible token on Stacks

;; Define the fungible token
(define-fungible-token reflekt-token)

;; Constants
(define-constant contract-owner tx-sender)
(define-constant err-owner-only (err u100))
(define-constant err-not-authorized (err u101))
(define-constant err-insufficient-balance (err u102))
(define-constant err-invalid-recipient (err u103))

;; Data variables
(define-data-var token-name (string-ascii 32) "Reflekt Token")
(define-data-var token-symbol (string-ascii 10) "RFLKT")
(define-data-var token-decimals uint u8)
(define-data-var token-uri (optional (string-utf8 256)) none)

;; SIP-010 Trait
(impl-trait 'SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE.sip-010-trait-ft-standard.sip-010-trait)

;; Public Functions

;; Transfer tokens
(define-public (transfer (amount uint) (sender principal) (recipient principal) (memo (optional (buff 34))))
    (begin
        ;; Verify sender authorization
        (asserts! (or (is-eq tx-sender sender) (is-eq contract-caller sender)) err-not-authorized)

        ;; Verify recipient is valid
        (asserts! (not (is-eq recipient sender)) err-invalid-recipient)

        ;; Perform the transfer
        (try! (ft-transfer? reflekt-token amount sender recipient))

        ;; Print memo if provided
        (match memo to-print (print to-print) 0x)

        ;; Print transfer event
        (print {
            action: "transfer",
            sender: sender,
            recipient: recipient,
            amount: amount
        })

        (ok true)
    )
)

;; Get token name
(define-read-only (get-name)
    (ok (var-get token-name))
)

;; Get token symbol
(define-read-only (get-symbol)
    (ok (var-get token-symbol))
)

;; Get token decimals
(define-read-only (get-decimals)
    (ok (var-get token-decimals))
)

;; Get token balance
(define-read-only (get-balance (account principal))
    (ok (ft-get-balance reflekt-token account))
)

;; Get total supply
(define-read-only (get-total-supply)
    (ok (ft-get-supply reflekt-token))
)

;; Get token URI
(define-read-only (get-token-uri)
    (ok (var-get token-uri))
)

;; Administrative Functions

;; Mint tokens (owner only)
(define-public (mint (amount uint) (recipient principal))
    (begin
        ;; Only contract owner can mint
        (asserts! (is-eq tx-sender contract-owner) err-owner-only)

        ;; Verify recipient is valid
        (asserts! (not (is-eq recipient contract-owner)) err-invalid-recipient)

        ;; Mint tokens
        (try! (ft-mint? reflekt-token amount recipient))

        ;; Print mint event
        (print {
            action: "mint",
            recipient: recipient,
            amount: amount
        })

        (ok true)
    )
)

;; Burn tokens
(define-public (burn (amount uint) (owner principal))
    (begin
        ;; Verify authorization
        (asserts! (or (is-eq tx-sender owner) (is-eq tx-sender contract-owner)) err-not-authorized)

        ;; Burn tokens
        (try! (ft-burn? reflekt-token amount owner))

        ;; Print burn event
        (print {
            action: "burn",
            owner: owner,
            amount: amount
        })

        (ok true)
    )
)

;; Set token URI (owner only)
(define-public (set-token-uri (new-uri (optional (string-utf8 256))))
    (begin
        (asserts! (is-eq tx-sender contract-owner) err-owner-only)
        (var-set token-uri new-uri)
        (ok true)
    )
)

;; Initialize contract (mint initial supply to owner)
(begin
    (try! (ft-mint? reflekt-token u1000000000000 contract-owner))
    (print {
        action: "initialized",
        total-supply: u1000000000000,
        owner: contract-owner
    })
)
