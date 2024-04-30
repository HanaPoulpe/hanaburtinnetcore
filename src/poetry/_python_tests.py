import fnmatch
import os
import pathlib
import subprocess
import sys
from collections.abc import Callable

from . import _utils as utils


def _add_unit_tests() -> set[str]:
    return {"**/tests/unit/**/test_*.py"}


def _add_integration_tests(folder: str) -> set[str]:
    return {
        f"**/tests/integration/**/{folder}/**/test_*.py",
        f"**/tests/integration/{folder}/**/test_*.py",
    }


def _add_functional_tests(folder: str) -> set[str]:
    return {
        f"**/tests/functional/**/{folder}/**/test_*.py",
        f"**/tests/functional/{folder}/**/test_*.py",
    }


def _add_common_tests(folder: str) -> set[str]:
    return _add_functional_tests(folder) | _add_integration_tests(folder)


@utils.sub_command_wrapper
def run_python_tests(test_patterns: set[str] | None = None, settings: str | None = None) -> None:
    if len(sys.argv) > 1:
        args = sys.argv[1:]
    elif test_patterns:
        args = []
        for p in test_patterns:
            args.extend(map((lambda x: str(x)), pathlib.Path(utils.PROJECT_DIR).glob(p)))
    else:
        args = ["tests"]

    if settings:
        # os.environ["DJANGO_CONFIGURATION"] = settings
        args.append(f"--dc={settings}")

    os.environ["ENV_FILE"] = os.path.join(utils.PROJECT_DIR, "tests", ".env")
    subprocess.check_call(["pytest"] + args, cwd=utils.PROJECT_DIR)


def run_unit_tests() -> None:
    run_python_tests(TestSuites.UNIT_TESTS[0], "UnitTest")


def run_interface_agnostic_tests() -> None:
    run_python_tests(TestSuites.INTERFACE_AGNOSTIC_TESTS[0], "InterfaceAgnostic")


def run_backoffice_tests() -> None:
    run_python_tests(TestSuites.BACKOFFICE_TESTS[0], "Backoffice")


def run_api_tests() -> None:
    run_python_tests(TestSuites.API_TESTS[0], "Api")


def _resolve_tests_for_file(filename: str) -> set[Callable[[], None]]:
    found_tests = set[Callable[[], None]]()
    for suite in dir(TestSuites):
        if suite.startswith("_") or not suite.isupper():
            continue

        patterns, tests = getattr(TestSuites, suite)
        if any(map((lambda p: fnmatch.fnmatch(filename, p)), patterns)):
            found_tests.add(tests)

    return found_tests


def run_tests_for_file() -> None:
    if len(sys.argv) < 2:
        raise ValueError("Please specify files to run tests for.")

    test_files = sys.argv[1:]
    all_tests: set[Callable[[], None]] = set()
    for file in test_files:
        all_tests |= _resolve_tests_for_file(file)
    errors: list[Exception] = []
    for test in all_tests:
        try:
            test()
        except Exception as e:
            errors.append(e)

    if errors:
        raise ExceptionGroup("Tests failures", errors)


def run_all_python_tests() -> None:
    errors = []
    all_tests = (
        TestSuites.UNIT_TESTS[1],
        TestSuites.INTERFACE_AGNOSTIC_TESTS[1],
        TestSuites.BACKOFFICE_TESTS[1],
        TestSuites.API_TESTS[1],
    )
    for test in all_tests:
        try:
            test()
        except Exception as e:
            errors.append(e)

    if errors:
        ExceptionGroup("Tests failures", errors)


class TestSuites:
    UNIT_TESTS = _add_unit_tests(), run_unit_tests
    INTERFACE_AGNOSTIC_TESTS = _add_common_tests("common"), run_interface_agnostic_tests
    BACKOFFICE_TESTS = (
        _add_common_tests("backoffice") | INTERFACE_AGNOSTIC_TESTS[0],
        run_backoffice_tests,
    )
    API_TESTS = (
        _add_common_tests("api") | INTERFACE_AGNOSTIC_TESTS[0],
        run_api_tests,
    )
