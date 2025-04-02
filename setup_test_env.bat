@echo off
echo Setting up test environment...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install test dependencies
echo Installing test dependencies...
pip install -r requirements-dev.txt

echo Test environment setup complete!
pause 