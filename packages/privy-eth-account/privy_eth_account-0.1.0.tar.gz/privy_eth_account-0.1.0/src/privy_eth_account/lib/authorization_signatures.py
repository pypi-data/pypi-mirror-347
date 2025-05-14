import json
import base64
from typing import Any, Dict, cast
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey

def canonicalize(obj: Any) -> str:
    """Simple JSON canonicalization function.
    
    Sorts dictionary keys and ensures consistent formatting.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def get_authorization_signature(
    url: str,
    body: Dict[str, Any],
    app_id: str,
    private_key: str,
) -> str:
    """Generate authorization signature for Privy API requests using ECDSA and hashlib.
    
    Args:
        url: The URL of the request
        body: The request body
        app_id: The Privy app ID
        private_key: The private key for authorization (without the 'wallet-auth:' prefix)
    
    Returns:
        The base64-encoded signature
    """
    # Construct the payload
    payload = {
        "version": 1,
        "method": "POST",
        "url": url,
        "body": body,
        "headers": {"privy-app-id": app_id},
    }

    # Serialize the payload to JSON
    serialized_payload = canonicalize(payload)

    # Create ECDSA P-256 signing key from private key
    private_key_pem = (
        f"-----BEGIN PRIVATE KEY-----\n{private_key}\n-----END PRIVATE KEY-----"
    )

    # Load the private key from PEM format
    private_key_obj = cast(
        EllipticCurvePrivateKey,
        serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"), password=None
        ),
    )

    # Sign the message using ECDSA with SHA-256
    signature = private_key_obj.sign(
        serialized_payload.encode("utf-8"), ec.ECDSA(hashes.SHA256())
    )

    # Convert the signature to base64 for easy transmission
    return base64.b64encode(signature).decode("utf-8") 