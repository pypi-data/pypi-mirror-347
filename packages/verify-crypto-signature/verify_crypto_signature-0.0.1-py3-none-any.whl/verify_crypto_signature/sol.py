from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.signature import Signature
from typing import Union, List


class VerifySOL:
    @staticmethod
    def is_address(public_key: Union[str, Pubkey]) -> bool:
        """
        Check if the given public key is valid

        Args:
            public_key (Union[str, Pubkey]): The public key to check

        Returns:
            bool: True if the public key is valid, False otherwise

        Raises:
            ValueError: If the public key is not a valid string or Pubkey
        """
        try:
            if isinstance(public_key, str):
                Pubkey.from_string(public_key)
            elif isinstance(public_key, Pubkey):
                pass
            else:
                raise ValueError("Validator: Invalid public key type")
            return True
        except ValueError as e:
            if "Validator" in str(e):
                raise e
            else:
                return False
        except Exception:
            return False
    
    @classmethod
    def sign_message(
        cls,
        message: Union[str, bytes],
        private_key: Union[str, bytes, List[Union[str, int]]]) -> Signature:
        """
        Sign a message using the given private key

        Args:
            message (Union[str, bytes]): The message to sign
            private_key (Union[str, bytes, List[Union[str, int]]]): The private key to sign the message with
        
        Returns:
            Signature: The signature of the message

        Raises:
            ValueError: If the message or private key is not valid
        """

        if isinstance(message, str):
            message = message.encode('utf-8')
            message = bytes(message)
        elif isinstance(message, bytes):
            pass
        else:
            raise ValueError("Validator: Invalid message type")
        
        if not isinstance(private_key, str) and not isinstance(private_key, bytes) and not isinstance(private_key, list):
            raise ValueError("Validator: Invalid private key type")
        
        keypair = cls.return_keypair(private_key)
        if keypair is None:
            raise ValueError("Validator: Invalid private key")
        
        return keypair.sign_message(message)
    @classmethod
    def verify_signature(
        cls,
        public_key: Union[str, Pubkey],
        message: Union[str, bytes],
        signature: Union[List[int], str, bytes, Signature]) -> bool:
        """
        Verify a signature of a message using the given public key

        Args:
            public_key (Union[str, Pubkey]): The public key to verify the signature with
            message (Union[str, bytes]): The message to verify the signature with
            signature (Union[List[int], bytes, Signature]): The signature to verify

        Returns:
            bool: True if the signature is valid, False otherwise

        Raises:
            ValueError: If the public key, message, or signature is not valid
        """
        if not isinstance(public_key, str) and not isinstance(public_key, Pubkey):
            raise ValueError("Validator: Invalid public key type")
        
        if not isinstance(message, str) and not isinstance(message, bytes):
            raise ValueError("Validator: Invalid message type")
        
        if not isinstance(signature, list) and not isinstance(signature, bytes) and not isinstance(signature, Signature) and not isinstance(signature, str):
            raise ValueError("Validator: Invalid signature type")
        
        if isinstance(public_key, str):
            public_key = Pubkey.from_string(public_key)
        
        if isinstance(signature, bytes):
            signature_object = Signature.from_bytes(signature)
        elif isinstance(signature, list):
            signature_object = Signature.from_bytes(bytes(signature))
        elif isinstance(signature, str):
            signature_object = Signature.from_string(signature)
        else:
            signature_object = signature

        if isinstance(message, str):
            message_bytes = message.encode('utf-8')
        elif isinstance(message, bytes):
            message_bytes = message

        return signature_object.verify(
            pubkey=public_key,
            message_bytes=message_bytes
        )

    @staticmethod
    def return_keypair(private_key: Union[str, list[Union[str, int]], bytes, bytearray]) -> Union[Keypair, None]:
        """
        Return a Keypair object from the given private key

        Args:
            private_key (Union[str, list[Union[str, int]]]): The private key to return the Keypair from

        Returns:
            Union[Keypair, None]: The Keypair object or None if the private key is not valid
        """
        if isinstance(private_key, str):
            try:
                formatted = [int(num) for num in private_key.replace('[', '').replace(']', '').replace(' ', '').split(',')]
                keypair = Keypair.from_bytes(bytearray(formatted))
            except:
                try:
                    keypair = Keypair.from_seed(private_key)
                except:
                    try:
                        keypair = Keypair.from_seed([word for word in private_key.split(' ')])
                    except:
                        try:
                            keypair = Keypair.from_base58_string(private_key)
                        except:
                            keypair = None
        elif isinstance(private_key, bytes):
            try:
                keypair = Keypair.from_seed(private_key)
            except:
                try:
                    keypair = Keypair.from_bytes(private_key)
                except:
                    keypair = None
        elif isinstance(private_key, bytearray):
            try:
                keypair = Keypair.from_bytes(private_key)
            except:
                keypair = None
        elif isinstance(private_key, list):
            try:
                keypair = Keypair.from_bytes(bytearray(private_key))
            except:
                try:
                    keypair = Keypair.from_seed(private_key)
                except:
                    keypair = None
        else:
            keypair = None
        return keypair
