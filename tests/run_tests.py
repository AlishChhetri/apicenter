#!/usr/bin/env python3
"""Test runner for APICenter with coverage reporting."""

import unittest
import os
import sys
import argparse
import time

try:
    import coverage

    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False


def print_header(text):
    """Print a nicely formatted header."""
    line = "=" * 70
    print(f"\n{line}\n{text.center(70)}\n{line}")


def run_tests(with_coverage=False, show_slow=False, pattern="test_*.py"):
    """Run all test cases with optional coverage reporting.

    Args:
        with_coverage: Whether to run tests with coverage reporting
        show_slow: Whether to show slow tests (>0.1s)
        pattern: File pattern to match for test files

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add parent directory to path to make the imports work
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, root_dir)

    if with_coverage and COVERAGE_AVAILABLE:
        print_header("Running tests with coverage")
        cov = coverage.Coverage(source=["apicenter"], omit=["*/tests/*"])
        cov.start()
    else:
        if with_coverage and not COVERAGE_AVAILABLE:
            print("Coverage package not available. Install with 'pip install coverage'.")
        print_header("Running tests")

    # Find all test cases
    start_time = time.time()
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern=pattern)

    # Set up a custom test result class to track durations if needed
    class TimingTextTestResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.test_timings = {}

        def startTest(self, test):
            self._started_at = time.time()
            super().startTest(test)

        def stopTest(self, test):
            self._stopped_at = time.time()
            self.test_timings[test.id()] = self._stopped_at - self._started_at
            super().stopTest(test)

    # Run the tests
    test_runner = unittest.TextTestRunner(
        verbosity=2, resultclass=TimingTextTestResult if show_slow else unittest.TextTestResult
    )
    result = test_runner.run(test_suite)

    # Print test duration
    total_time = time.time() - start_time
    print(f"\nRan {result.testsRun} tests in {total_time:.3f}s")

    # Show slow tests if requested
    if show_slow and hasattr(result, "test_timings"):
        print("\nSlow tests (>0.1s):")
        slow_tests = {k: v for k, v in result.test_timings.items() if v > 0.1}
        if slow_tests:
            for test_id, duration in sorted(slow_tests.items(), key=lambda x: x[1], reverse=True):
                print(f"  {test_id}: {duration:.3f}s")
        else:
            print("  None")

    # Generate coverage report if requested
    if with_coverage and COVERAGE_AVAILABLE:
        print_header("Coverage Report")
        cov.stop()
        cov.report()

        # Generate HTML report
        html_dir = os.path.join(os.path.dirname(__file__), "coverage_html")
        cov.html_report(directory=html_dir)
        print(f"\nHTML coverage report generated in {html_dir}")

    # Show test results summary
    if result.errors or result.failures:
        print_header("Test Results: FAILED")
        print(f"Errors: {len(result.errors)}")
        print(f"Failures: {len(result.failures)}")
    else:
        print_header("Test Results: PASSED")

    # Return success or failure
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run APICenter tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage reporting")
    parser.add_argument("--show-slow", action="store_true", help="Show slow tests (>0.1s)")
    parser.add_argument("--pattern", type=str, default="test_*.py", help="Test file pattern")

    args = parser.parse_args()
    sys.exit(run_tests(with_coverage=args.coverage, show_slow=args.show_slow, pattern=args.pattern))
