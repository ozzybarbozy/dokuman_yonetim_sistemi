import pytest
import os
import sys

def run_tests():
    """Run all tests in the tests directory."""
    # Get the directory containing this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Add the project root directory to the Python path
    sys.path.insert(0, current_dir)
    
    # Change to the project root directory
    os.chdir(current_dir)
    
    # Run pytest with specific options
    pytest.main([
        'tests',  # Directory containing tests
        '-v',     # Verbose output
        '--cov=src.app',  # Coverage for app package
        '--cov-report=term',  # Show coverage in terminal
        '--cov-report=html'   # Generate HTML coverage report
    ])

if __name__ == '__main__':
    run_tests() 