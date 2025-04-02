import subprocess
import os
from datetime import datetime

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        return None

def auto_push():
    print("Starting automatic push process...")
    
    # Get current timestamp for commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Step 1: Add all changes
    print("Adding changes...")
    run_command("git add .")
    
    # Step 2: Commit changes
    print("Committing changes...")
    commit_message = f"Auto commit: {timestamp}"
    run_command(f'git commit -m "{commit_message}"')
    
    # Step 3: Push to GitHub
    print("Pushing to GitHub...")
    run_command("git push origin main")
    
    print("Push completed successfully!")

if __name__ == "__main__":
    auto_push() 