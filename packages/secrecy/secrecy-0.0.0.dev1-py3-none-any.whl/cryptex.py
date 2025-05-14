"""Cryptex

Interfaces for file en-/decryption.
"""
import base64
import os
import sys
from pathlib import Path
from typing import Optional

import click
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Set up application directories
DATA_DIR: Path = Path("~/cryptex").expanduser()
ENCRYPTION_DIR = Path(DATA_DIR, "encrypted")
DECRYPTION_DIR = Path(DATA_DIR, "decrypted")

# Create directories if they don't exist
for directory in [DATA_DIR, ENCRYPTION_DIR, DECRYPTION_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def generate_key(password: bytes, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
    """Generate an encryption key from a password.
    
    Args:
        password: The password to derive the key from
        salt: Optional salt bytes. If not provided, new random salt will be generated
        
    Returns:
        A tuple of (key, salt)
    """
    # Generate a new salt if none is provided
    if salt is None:
        salt = os.urandom(16)
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1_200_000
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, salt


@click.group()
def cli():
    """Cryptex - A tool for encrypting and decrypting files."""
    pass


@cli.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--password', '-p', help='Encryption password')
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file path (defaults to DATA_DIR/encrypted/filename.crypt)')
def encrypt(file: Path, password: Optional[str], output: Optional[Path]):
    """Encrypt a file using a password."""
    # Get or prompt for password
    if not password:
        password = click.prompt('Enter encryption password', hide_input=True, 
                               confirmation_prompt=True)
    
    password_bytes = password.encode()
    
    # Generate key and salt
    key, salt = generate_key(password_bytes)
    f = Fernet(key)
    
    # Read the input file
    with open(file, "r") as input_file:
        token = f.encrypt(input_file.read().encode())
    
    # Determine output path
    if not output:
        output = ENCRYPTION_DIR / f"{file.stem}.crypt"
    
    # Write both the salt and encrypted data to the file
    with open(output, "wb") as output_file:
        output_file.write(salt)  # First 16 bytes will be the salt
        output_file.write(token)  # Rest is the encrypted data
    
    click.echo(f"Encrypted {file} successfully.")
    click.echo(f"Saved output to {output.resolve()}")


@cli.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option('--password', '-p', help='Decryption password')
@click.option('--output', '-o', type=click.Path(path_type=Path), 
              help='Output file path (used only if user chooses to save)')
@click.option('--print-only', '-P', is_flag=True, default=False,
              help='Print decrypted content to console without prompting to save')
def decrypt(file: Path, password: Optional[str], output: Optional[Path], print_only: bool):
    """Decrypt an encrypted file using a password."""
    # Get or prompt for password
    if not password:
        password = click.prompt('Enter decryption password', hide_input=True)
    
    password_bytes = password.encode()
    
    # Read the encrypted file
    try:
        with open(file, "rb") as input_file:
            # Read the salt from the first 16 bytes
            salt = input_file.read(16)
            # Read the rest as encrypted data
            encrypted_data = input_file.read()
        
        # Generate the key with the extracted salt
        key, _ = generate_key(password_bytes, salt)
        f = Fernet(key)
        
        # Decrypt the data
        decrypted_data = f.decrypt(encrypted_data)
        decrypted_text = decrypted_data.decode()
        
        # Print the decrypted data
        click.echo("\n=================== DECRYPTED DATA ====================\n")
        click.echo(decrypted_text)
        click.echo("\n=======================================================\n")
        
        # If print-only flag is set, don't prompt to save
        if print_only:
            return
            
        # Prompt user if they'd like to save the output
        if click.confirm("Would you like to save this output to disk?", default=True):
            # Determine output path - either use provided path or prompt user
            if not output:
                suggested_path = DECRYPTION_DIR / f"{file.stem}_decrypted.txt"
                path_prompt = (
                    "Where? (Enter an absolute path, or press enter to use\n"
                    f"the Cryptex data directory: {suggested_path})"
                )
                output_str = click.prompt(path_prompt, default=str(suggested_path), show_default=False)
                output = Path(output_str).expanduser()
            
            # Ensure parent directory exists
            try:
                output.parent.mkdir(parents=True, exist_ok=True)
                
                # Confirm before overwriting
                if output.exists() and not click.confirm(f"File {output} already exists. Overwrite?"):
                    click.echo("Operation cancelled.")
                    return
                
                # Write decrypted data to file
                with open(output, "w") as output_file:
                    output_file.write(decrypted_text)
                
                click.echo(f"✓ Wrote decrypted data to {output.resolve()}")
            except Exception as e:
                click.echo(f"Error saving file: {e}", err=True)
                return
    
    except Exception as e:
        click.echo(f"Error decrypting file: {e}", err=True)
        click.echo("This could be due to an incorrect password or corrupted file.", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
