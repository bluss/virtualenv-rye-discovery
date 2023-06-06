"""
Virtualenv plugin for discovery of Python interpreters through Rye.
"""

import logging
import subprocess
import sys

from virtualenv.discovery.discover import Discover
from virtualenv.discovery.py_spec import PythonSpec
from virtualenv.discovery.py_info import PythonInfo

LOGGER = logging.getLogger()


class RyeDiscovery(Discover):
    """
    Virtualenv plugin for discovery of Python interpreters through Rye.

    Find existing or fetch if missing with Rye.
    """
    def __init__(self, options):
        super().__init__(options)
        self.python_spec = options.python if options.python else [sys.executable]
        self.app_data = options.app_data

    @classmethod
    def add_parser_arguments(cls, parser):
        parser.add_argument(
            "-p",
            "--python",
            dest="python",
            metavar="py",
            type=str,
            action="append",
            default=[],
            help="interpreter based on what to create environment (path/identifier) "
            "- by default use the interpreter where the tool is installed - first found wins",
        )

    def run(self):
        # 1. rye fetch  (no network request if already installed)
        # 2. rye toolchain list
        for python_spec in self.python_spec:
            spec = PythonSpec.from_string_spec(python_spec)
            LOGGER.debug("find python for spec: %r, %r", python_spec, spec)
            if spec.path:
                # If path is set, just accept it
                py_info = PythonInfo.from_exe(spec.path, self.app_data, env=self._env)
                LOGGER.debug("found python: %r", py_info)
                return py_info
            else:
                # try fetch the interpreter if possible
                fetch_cmd = ["rye", "fetch", fetch_version(spec)]
                LOGGER.info("Running: %r", " ".join(fetch_cmd))
                rye_fetch = subprocess.run(fetch_cmd)
                if rye_fetch.returncode != 0:
                    continue

            list_cmd = ["rye", "toolchain", "list"]
            LOGGER.info("Running: %r", " ".join(list_cmd))
            rye_list = subprocess.run(list_cmd, capture_output=True, encoding="utf-8", errors="replace")
            if rye_list.returncode != 0:
                LOGGER.error("Error on rye list (return code: %r)\n%s\n%s\n", rye_list.returncode,
                             rye_list.stdout, rye_list.stderr)
                continue
            LOGGER.debug("%s", rye_list.stdout)

            matching_exe = find_match_from_rye(rye_list.stdout, spec)
            if matching_exe is not None:
                py_info = PythonInfo.from_exe(matching_exe, self.app_data, env=self._env)
                LOGGER.debug("found python: %r", py_info)
                return py_info

        return None


def find_match_from_rye(rye_list, python_spec: PythonSpec):
    """
    From rye toolchain list output, find matching python version.
    """
    for line in rye_list.splitlines():
        rye_py_version, rye_py_path = line.split(None, maxsplit=1)
        # turn cpython@3.8 into cpython3.8 which PythonSpec wants
        py_version = rye_py_version.replace("@", "")
        version_spec = PythonSpec.from_string_spec(py_version)
        if version_spec.satisfies(python_spec):
            # use Rye's path output since it can vary where it's installed
            exe_path = rye_py_path.strip(" ()")
            return exe_path


def fetch_version(python_spec: PythonSpec):
    "return a string such as 3.9 or cpython@3.9 that rye can fetch"
    vers = ""
    if python_spec.implementation:
        vers += python_spec.implementation + "@"
    vers += str(python_spec.major)
    if python_spec.minor is not None:
        vers += "." + str(python_spec.minor)
        if python_spec.micro is not None:
            vers += "." + str(python_spec.micro)
    return vers
