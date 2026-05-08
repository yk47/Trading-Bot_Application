#!/usr/bin/env python3
"""
Setup script for Trading Bot.

This script helps set up the trading bot by:
1. Creating a virtual environment
2. Installing dependencies
3. Creating a .env file with user's API credentials
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(cmd, shell=False):
    """Run a command and return success status."""
    try:
        subprocess.run(cmd, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Error: {e}")
        return False


def main():
    """Main setup function."""
    print("=" * 60)
    print("Trading Bot Setup")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    
    # Step 1: Create virtual environment
    print("\n[1/3] Creating virtual environment...")
    venv_path = project_root / "venv"
    
    if venv_path.exists():
        print(f"Virtual environment already exists at {venv_path}")
    else:
        if not run_command([sys.executable, "-m", "venv", str(venv_path)]):
            print("Failed to create virtual environment")
            return False
        print(f"✓ Virtual environment created at {venv_path}")
    
    # Step 2: Install dependencies
    print("\n[2/3] Installing dependencies...")
    
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip"
    else:
        pip_path = venv_path / "bin" / "pip"
    
    requirements_file = project_root / "requirements.txt"
    
    if not run_command([str(pip_path), "install", "-r", str(requirements_file)]):
        print("Failed to install dependencies")
        return False
    
    print("✓ Dependencies installed")
    
    # Step 3: Create .env file
    print("\n[3/3] Setting up API credentials...")
    
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if env_file.exists():
        print(f"API credentials file already exists at {env_file}")
        overwrite = input("Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Skipping API credentials setup")
            return True
    
    # Get API credentials from user
    print("\nTo get your testnet API credentials:")
    print("1. Go to https://testnet.binancefuture.com")
    print("2. Login/Register")
    print("3. Go to Account > API Management")
    print("4. Create a new API key")
    
    api_key = input("\nEnter your Binance API Key: ").strip()
    api_secret = input("Enter your Binance API Secret: ").strip()
    
    if not api_key or not api_secret:
        print("Error: API key and secret cannot be empty")
        return False
    
    # Create .env file
    env_content = f"""# Binance Futures Testnet API Credentials
BINANCE_API_KEY={api_key}
BINANCE_API_SECRET={api_secret}
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✓ API credentials saved to {env_file}")
    
    # Final message
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nNext steps:")
    
    if sys.platform == "win32":
        print(f"1. Activate virtual environment: .\\venv\\Scripts\\activate")
    else:
        print(f"1. Activate virtual environment: source venv/bin/activate")
    
    print("2. Test connection: python cli.py test-connection")
    print("3. Place an order: python cli.py place-order")
    print("\nFor more help, see README.md")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
