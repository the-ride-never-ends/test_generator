#!/bin/bash
# Script to run tests, type checking, and linting for Test Generator Mk2

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Create reports directory if it doesn't exist
mkdir -p test_reports

# Default values
RUN_TESTS=true
RUN_MYPY=false
RUN_FLAKE8=false
VERBOSITY_ARG=""
CHECK_ALL=false
RESPECT_GITIGNORE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -q|--quiet)
            VERBOSITY_ARG="-q"
            shift
            ;;
        --mypy)
            RUN_MYPY=true
            shift
            ;;
        --flake8)
            RUN_FLAKE8=true
            shift
            ;;
        --check-all)
            CHECK_ALL=true
            RUN_MYPY=true
            RUN_FLAKE8=true
            shift
            ;;
        --lint-only)
            RUN_TESTS=false
            RUN_MYPY=true
            RUN_FLAKE8=true
            shift
            ;;
        --respect-gitignore)
            RESPECT_GITIGNORE=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [-q|--quiet] [--mypy] [--flake8] [--check-all] [--lint-only] [--respect-gitignore]"
            exit 1
            ;;
    esac
done

# Overall exit code
OVERALL_EXIT=0

# Run the tests if requested
if $RUN_TESTS; then
    echo "Running tests for Test Generator..."
    python utils/for_tests/run_tests.py $VERBOSITY_ARG
    
    # Get the exit code
    TEST_EXIT_CODE=$?
    
    # If tests passed
    if [ $TEST_EXIT_CODE -eq 0 ]; then
        echo -e "\n✅ All tests passed!"
    else
        echo -e "\n❌ Tests failed with exit code $TEST_EXIT_CODE"
        OVERALL_EXIT=1
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
fi

# Run linting tools if requested
if $RUN_MYPY || $RUN_FLAKE8; then
    echo -e "\n==== Running linting tools ===="
    
    # Build the command
    LINT_CMD="python utils/for_tests/lint_report.py"
    if $RESPECT_GITIGNORE; then
        LINT_CMD="$LINT_CMD --respect-gitignore"
    fi
    
    # Run the linting command
    eval $LINT_CMD
    LINT_EXIT_CODE=$?
    
    if [ $LINT_EXIT_CODE -eq 0 ]; then
        echo -e "\n✅ All linting checks passed!"
    else
        echo -e "\n❌ Linting failed with exit code $LINT_EXIT_CODE"
        OVERALL_EXIT=1
    fi
    
    # Show the latest lint report
    if [ -f "test_reports/latest_lint_report.md" ]; then
        echo -e "\nLatest lint report is available at: test_reports/latest_lint_report.md"
        
        # If we have a markdown viewer, show the report
        if command -v glow &> /dev/null; then
            echo -e "\nShowing lint report preview:"
            glow test_reports/latest_lint_report.md
        elif command -v bat &> /dev/null; then
            echo -e "\nShowing lint report preview:"
            bat test_reports/latest_lint_report.md
        elif command -v less &> /dev/null; then
            echo -e "\nShowing lint report preview (press q to exit):"
            less test_reports/latest_lint_report.md
        else
            echo -e "\nTo view the full lint report, open test_reports/latest_lint_report.md in a text editor."
        fi
    fi
fi

# Show usage help if nothing was run
if ! $RUN_TESTS && ! $RUN_MYPY && ! $RUN_FLAKE8; then
    echo "Usage: $0 [-q|--quiet] [--mypy] [--flake8] [--check-all] [--lint-only] [--respect-gitignore]"
    echo ""
    echo "Options:"
    echo "  -q, --quiet           Run tests with reduced verbosity"
    echo "  --mypy                Run mypy type checking"
    echo "  --flake8              Run flake8 linting"
    echo "  --check-all           Run tests, type checking, and linting"
    echo "  --lint-only           Run only type checking and linting (no tests)"
    echo "  --respect-gitignore   Ignore files/folders listed in .gitignore during linting"
fi

exit $OVERALL_EXIT


