#!/bin/bash
# Script to run tests for Test Generator Mk2 with reporting

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Create reports directory if it doesn't exist
mkdir -p test_reports

# Check for arguments
VERBOSITY_ARG=""
if [ "$1" == "-q" ]; then
    VERBOSITY_ARG="-q"
fi

# Run the tests
echo "Running tests for Test Generator..."
python utils/for_tests/run_tests.py $VERBOSITY_ARG

# Get the exit code
EXIT_CODE=$?

# If tests passed
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n✅ All tests passed!"
else
    echo -e "\n❌ Tests failed with exit code $EXIT_CODE"
fi

# Show the latest report
if [ -f "test_reports/latest_report.md" ]; then
    echo -e "\nLatest report is available at: test_reports/latest_report.md"
    
    # If we have a markdown viewer, show the report
    if command -v glow &> /dev/null; then
        echo -e "\nShowing report preview:"
        glow test_reports/latest_report.md
    elif command -v bat &> /dev/null; then
        echo -e "\nShowing report preview:"
        bat test_reports/latest_report.md
    elif command -v less &> /dev/null; then
        echo -e "\nShowing report preview (press q to exit):"
        less test_reports/latest_report.md
    else
        echo -e "\nTo view the full report, open test_reports/latest_report.md in a text editor."
    fi
fi





