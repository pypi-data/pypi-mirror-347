# Verify Crypto Signature

A Python library for verifying and working with cryptographic signatures, currently supporting EVM and Solana blockchain signatures.

## Features

- Verify message signatures from EVM and Solana addresses
- Sign messages using private keys
- Recover wallet addresses from signatures (Only supports EVM)
- Validate EVM and Solana addresses

## Installation

```bash
pip install verify-crypto-signature
```

## Dependencies

- eth_account
- eth_utils
- eth_keys
- solders

## Usage

### Verifying an EVM Signature

```python
from verify_crypto_signature.evm import VerifyEVM

# Verify if a message was signed by a specific address
wallet_address = "0x..."  # Example address
message = "Hello, world!"
signature = "0x..."  # Signature obtained from the wallet

# Verify the signature
is_valid = VerifyEVM.verify_signature(wallet_address, message, signature)
if is_valid:
    print("Signature is valid")
else:
    print("Signature is invalid")
```

### Signing a Message

```python
from verify_crypto_signature.evm import VerifyEVM

# Sign a message with a private key
private_key = "0x..."  # Your private key (keep this secret!)
message = "Hello, world!"

# Sign the message
signed_message = VerifyEVM.sign_message(message, private_key)
signature = signed_message.signature.hex()
print(f"Signature: {signature}")
```

### Recovering an Address from a Signature (Only supports EVM)

```python
from verify_crypto_signature.evm import VerifyEVM

# Recover the signer's address
message = "Hello, world!"
signature = "0x..."  # The signature

address = VerifyEVM.get_address_from_message(message, signature=signature)
print(f"Signer address: {address}")
```

### Verifying a Solana Signature

```python
from verify_crypto_signature.sol import VerifySOL

# Verify if a message was signed by a specific address
wallet_address = "5yQ6...."  # Example address
message = "Hello, world!"
signature = "4K2...."  # Signature obtained from the wallet

# Verify the signature
is_valid = VerifySOL.verify_signature(wallet_address, message, signature)
```

### Signing a Message

```python
from verify_crypto_signature.sol import VerifySOL

# Sign a message with a private key
private_key = "4K2...."  # Your private key (keep this secret!)
message = "Hello, world!"

# Sign the message
signed_message = VerifySOL.sign_message(message, private_key)
```
## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 