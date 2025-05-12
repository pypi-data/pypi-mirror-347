from eth_account.account import Account
from eth_account.messages import encode_defunct
from eth_account.datastructures import SignedMessage
from eth_utils.address import is_address
from eth_keys.datatypes import PrivateKey
from typing import Union, Optional, Tuple

VRS = Union[str, bytes, int]

class VerifyEVM:
    @staticmethod
    def is_address(wallet_address: str) -> bool:
        """
        Check if the given wallet address is valid

        Args:
            wallet_address (str): The wallet address to check

        Returns:
            bool: True if the wallet address is valid, False otherwise

        Raises:
            ValueError: If the wallet address is not a valid string
        """
        return is_address(wallet_address)
    
    @staticmethod
    def sign_message(
            message: str,
            private_key: Union[str, bytes, int, PrivateKey]) -> SignedMessage:
        """
        Sign a message using the given private key

        Args:
            message (str): The message to sign
            private_key (Union[str, bytes, int, PrivateKey]): The private key to sign the message with

        Returns:
            SignedMessage: The signed message

        Raises:
            ValueError: If the message or private key is not valid
        """
        return Account.sign_message(
            message=encode_defunct(text=message),
            private_key=private_key
        )

    @classmethod
    def verify_signature(
            cls,
            wallet_address: str,
            message: str,
            signature: Union[str, bytes, int]) -> bool:
        """
        Verify a signature of a message using the given wallet address

        Args:
            wallet_address (str): The wallet address to verify the signature with
            message (str): The message to verify the signature with
            signature (Union[str, bytes, int]): The signature to verify

        Returns:
            bool: True if the signature is valid, False otherwise

        Raises:
            ValueError: If the wallet address, message, or signature is not valid
        """
        if not cls.is_address(wallet_address):
            raise ValueError("Validator: wallet_address must be a valid address")
        signer_address = cls.get_address_from_message(message, signature)
        return signer_address.lower() == wallet_address.lower()

    @staticmethod
    def get_address_from_message(
            message: str,
            vrs: Optional[Tuple[VRS, VRS, VRS]] = None,
            signature: Optional[Union[str, bytes, int]] = None) -> str:
        """
        Get the address from a message using the given vrs or signature

        Args:
            message (str): The message to get the address from
            vrs (Optional[Tuple[VRS, VRS, VRS]]): The vrs to get the address from
            signature (Optional[Union[str, bytes, int]]): The signature to get the address from

        Returns:
            str: The address from the message

        Raises:
            ValueError: If the vrs or signature is not valid, or if both or none are provided
        """
        if vrs is None and signature is None:
            raise ValueError("Validator: Either vrs or signature must be provided")
        if vrs is not None and signature is not None:
            raise ValueError("Validator: Only one of vrs or signature must be provided")
        if vrs is not None:
            return Account.recover_message(
                encode_defunct(text=message),
                vrs=vrs
            )
        if signature is not None:
            return Account.recover_message(
                encode_defunct(text=message),
                signature=signature
            )

