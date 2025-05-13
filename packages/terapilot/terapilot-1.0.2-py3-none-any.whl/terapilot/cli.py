#!/usr/bin/env python3
import cohere
from cohere.core import ApiError as CohereError
import subprocess
import os
import re
import sys
import warnings
import getpass
from pathlib import Path
from requests import RequestsDependencyWarning
from dotenv import load_dotenv
from typing import Tuple

# Constants
CONFIG_DIR = Path.home() / ".config" / "terapilot"
CONFIG_FILE = CONFIG_DIR / "config.env"
COHERE_SIGNUP_URL = "https://dashboard.cohere.com/signup"
GITHUB_URL = "https://github.com/akhilesh2220/terapilot"
SUPPORT_EMAIL = "akhileshs222000@gmail.com"
VERSION = "1.0.0"

def clean_command(output: str) -> str:
    """Sanitize the AI-generated command"""
    return re.sub(r"```(bash|shell)?|['\"]", "", output).strip()

def generate_command(co: cohere.Client, prompt: str) -> str:
    """Convert natural language to shell command"""
    try:
        response = co.generate(
            model="command-r-plus",
            prompt=f"Convert this to a Linux command: {prompt}. Provide ONLY the command.",
            max_tokens=100,
            temperature=0.2,
            stop_sequences=["\n"]
        )
        return clean_command(response.generations[0].text)
    except CohereError as e:
        print(f"\n🔴 Cohere API Error: {e.message}", file=sys.stderr)
        sys.exit(1)

def setup_config() -> None:
    """Create config directory if needed"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.touch(exist_ok=True)
    CONFIG_FILE.chmod(0o600)  # Restrict to owner only

def load_config() -> str:
    """Load API key with proper precedence"""
    # 1. Check environment variable
    if "COHERE_API_KEY" in os.environ:
        return os.environ["COHERE_API_KEY"]
    
    # 2. Check config files
    config_paths = [
        CONFIG_FILE,
        Path(".env"),
        Path(__file__).parent.parent / ".env"
    ]
    
    for path in config_paths:
        if path.exists():
            load_dotenv(path, override=True)
            if "COHERE_API_KEY" in os.environ:
                return os.environ["COHERE_API_KEY"]
    
    # 3. No key found
    print("\n🔴 Error: No API key configured", file=sys.stderr)
    print("To get started:", file=sys.stderr)
    print(f"1. Get a free API key: {COHERE_SIGNUP_URL}", file=sys.stderr)
    print("2. Configure with: terapilot --config", file=sys.stderr)
    sys.exit(1)

def execute_command(command: str) -> int:
    """Execute shell command with better error handling and sudo support"""
    try:
        if "sudo" in command.lower():
            # Run in interactive mode for sudo (allows password prompt)
            print("\n⚠️ Running 'sudo' command - enter password if prompted:")
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                # Use stdin from terminal for password input
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
            )
        else:
            # Non-interactive mode (captures output)
            result = subprocess.run(
                command,
                shell=True,
                check=False,
                capture_output=True,
                text=True,
            )
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"⚠️ {result.stderr}", file=sys.stderr)
        
        return result.returncode
    except Exception as e:
        print(f"🚨 Command execution failed: {str(e)}", file=sys.stderr)
        return 1

def validate_api_key(key: str) -> Tuple[bool, str]:
    """Check if API key is valid by making a test call to Cohere"""
    try:
        test_client = cohere.Client(key)
        test_client.generate(
            model="command-r-plus",
            prompt="test",
            max_tokens=1,
            temperature=0.1
        )
        return True, "✅ Key is valid and has API access"
    except CohereError as e:
        if e.status_code == 401:
            return False, "🔴 Invalid API key (unauthorized)"
        elif e.status_code == 403:
            return False, "🔴 Key valid but insufficient permissions"
        elif e.status_code == 429:
            return False, "⚠️ Key valid but rate limited"
        else:
            return False, f"⚠️ API error: {e.message}"
    except Exception as e:
        return False, f"⚠️ Connection failed: {str(e)}"

def run_config_wizard() -> None:
    """Interactive API key configuration with validation"""
    setup_config()
    print(f"\n🔧 Terapilot Configuration")
    
    try:
        current_key = load_config()
        print(f"Current key: {current_key[:4]}...{current_key[-4:]}")
        valid, msg = validate_api_key(current_key)
        print(f"Status: {msg}")
    except SystemExit:
        current_key = None
    
    while True:
        print("\nEnter new Cohere API key:")
        print("(Press Ctrl+C to cancel or leave blank to keep current)")
        new_key = getpass.getpass(prompt="> ").strip()
        
        if not new_key:
            print("\n❌ No key entered - configuration unchanged")
            return
        
        # Validate key format
        if len(new_key) != 40 or not new_key.isalnum():
            print(f"\n⚠️ Warning: Expected 40 alphanumeric characters, got {len(new_key)}")
            if not input("Continue without format validation? [y/N]: ").lower().startswith('y'):
                continue
        
        # Validate with Cohere servers
        print("\n🔍 Verifying API key with Cohere servers...")
        is_valid, validation_msg = validate_api_key(new_key)
        print(validation_msg)
        
        if not is_valid:
            if "rate limited" in validation_msg.lower():
                if input("Continue with this key anyway? [y/N]: ").lower().startswith('y'):
                    break
            continue
        
        # Save configuration
        with open(CONFIG_FILE, "w") as f:
            f.write(f"COHERE_API_KEY='{new_key}'\n")
        
        # Overwrite memory
        new_key = 'x' * len(new_key)
        
        print(f"\n✅ Configuration saved")
        print("Note: Environment variables take precedence over this file")
        break

def remove_config() -> None:
    """Remove the API key configuration"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        print(f"✅ Removed configuration file")
    else:
        print(f"ℹ️ No configuration file found")
    print("Note: Environment variables may still be set")

def show_help() -> None:
    """Display help information"""
    print(f"""\nTerapilot v{VERSION} - Natural Language to Shell Command

Usage:
  terapilot --config          # Configure API key
  terapilot --config-remove   # Remove saved API key
  terapilot --version         # Show version
  terapilot --help            # Show this help

Configuration:
  - Keys are saved to: {CONFIG_FILE}
  - Get API keys from: {COHERE_SIGNUP_URL}
  - Environment variable COHERE_API_KEY overrides config file

Support:
  - GitHub: {GITHUB_URL}
  - Report issues: {SUPPORT_EMAIL}

""")

def main():
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)

    # Handle special commands first
    if len(sys.argv) == 1:
        show_help()
        return
        
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"Terapilot v{VERSION}")
        return
    
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        return
    
    if "--config" in sys.argv:
        run_config_wizard()
        return
    
    if "--config-remove" in sys.argv:
        remove_config()
        return

    # Normal command processing
    try:
        api_key = load_config()  # This will show help if no key configured
        co = cohere.Client(api_key)
        
        # Filter out any remaining flags
        user_input = " ".join([a for a in sys.argv[1:] if not a.startswith("--")])
        
        if not user_input:
            show_help()
            return
            
        command = generate_command(co, user_input)
        print(f"\n🧠 Interpretation: {user_input}")
        print(f"⚡ Command: {command}\n")
        
        sys.exit(execute_command(command))
        
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n🔴 Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

