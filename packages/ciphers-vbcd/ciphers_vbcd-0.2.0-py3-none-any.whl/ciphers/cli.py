"""Command-line interface for the ciphers package."""

import os
import click
from typing import Any

from ciphers.cipher_service import CipherService


def _get_key_data(key: str) -> Any:
    """
    Determine if the key is a file path or a direct key value.

    Args:
        key: The key string which might be a file path or direct key

    Returns:
        The key data (either from file or the original key)

    Raises:
        FileNotFoundError: If the key appears to be a file path but the file doesn't exist
    """
    # Check if the key looks like a file path and the file exists
    if os.path.exists(key) and os.path.isfile(key):
        with open(key, "rb") as f:
            return f.read()

    # For Caesar cipher, convert to int if possible
    try:
        return int(key)
    except ValueError:
        # Not an integer, return as is (might be a string key or encoded data)
        return key


@click.group()
def cli() -> None:
    """Tool for encrypting and decrypting messages using various cipher algorithms."""
    pass


@cli.command()
@click.option("--algorithm", "-a", required=True, help="The cipher algorithm to use")
@click.option(
    "--key",
    "-k",
    required=True,
    help="The key for the cipher algorithm (can be a direct key or a file path)",
)
@click.argument("message")
def encrypt(algorithm: str, key: str, message: str) -> None:
    """Encrypt a message using the specified algorithm."""
    try:
        key_data = _get_key_data(key)

        result = CipherService.encrypt(message, algorithm, key_data)
        click.echo(result)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except FileNotFoundError:
        click.echo(f"Error: Key file '{key}' not found", err=True)


@cli.command()
@click.option("--algorithm", "-a", required=True, help="The cipher algorithm to use")
@click.option(
    "--key",
    "-k",
    required=True,
    help="The key for the cipher algorithm (can be a direct key or a file path)",
)
@click.argument("message")
def decrypt(algorithm: str, key: str, message: str) -> None:
    """Decrypt a message using the specified algorithm."""
    try:
        key_data = _get_key_data(key)

        result = CipherService.decrypt(message, algorithm, key_data)
        click.echo(result)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except FileNotFoundError:
        click.echo(f"Error: Key file '{key}' not found", err=True)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
