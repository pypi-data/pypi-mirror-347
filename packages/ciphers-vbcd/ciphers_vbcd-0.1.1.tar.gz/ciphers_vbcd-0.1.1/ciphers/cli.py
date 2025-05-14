"""Command-line interface for the ciphers package."""

import click

from ciphers.cipher_service import CipherService


@click.group()
def cli() -> None:
    """Tool for encrypting and decrypting messages using various cipher algorithms."""
    pass


@cli.command()
@click.option("--algorithm", "-a", required=True, help="The cipher algorithm to use")
@click.option("--key", "-k", required=True, help="The key for the cipher algorithm")
@click.argument("message")
def encrypt(algorithm: str, key: str, message: str) -> None:
    """Encrypt a message using the specified algorithm."""
    try:
        result = CipherService.encrypt(message, algorithm, key)
        click.echo(result)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)


@cli.command()
@click.option("--algorithm", "-a", required=True, help="The cipher algorithm to use")
@click.option("--key", "-k", required=True, help="The key for the cipher algorithm")
@click.argument("message")
def decrypt(algorithm: str, key: str, message: str) -> None:
    """Decrypt a message using the specified algorithm."""
    try:
        result = CipherService.decrypt(message, algorithm, key)
        click.echo(result)
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
