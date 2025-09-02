from hashlib import sha256
from typing import Literal


def get_checksum(
        data: bytes,
        *,
        algo: Literal["sha256"] = "sha256",  # type: ignore[arg-type]
        ) -> str:
    """
    Calculates the hash of a byte string and returns it (with an algorithm id).
    
    Currently only sha256 is supported.
    """
    return f"sha256:{sha256(data).hexdigest()}"


def verify_checksum(
        data: bytes,
        hash: str,
        ) -> bool:
    """
    Verifies that the hash of a byte string agrees with a given value.
    
    The hash is always prefixed with an algorith id.
    Currently only sha256 is supported.
    """
    for algo in ["sha256"]:  # type: ignore[assignment]
        if hash.startswith(f"{algo}:"):
            ref = get_checksum(data, algo=algo)  # type: ignore[arg-type]
            return hash == ref
    return False

# Note: mypy doesn't even accept a string constant for a Literal argument.
# Only a type-ignore comment seems to help.
# ty gets it right.
