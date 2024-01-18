import subprocess
import sys

from . import _utils as utils


@utils.sub_command_wrapper
def run_eslint() -> None:
    subprocess.check_call(["npm", "run", "eslint"] + sys.argv[1:], cwd=utils.SRC_DIR)


@utils.sub_command_wrapper
def run_js_tests() -> None:
    subprocess.check_call(["npm", "test"] + sys.argv[1:])
