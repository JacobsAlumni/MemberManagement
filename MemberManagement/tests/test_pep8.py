from __future__ import annotations

import os
import os.path
import unittest

import pycodestyle

ignore_patterns = (
    'venv', 'env', '.git', '__pycache__', 'migrations', 'node_modules')

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


class Pep8ComplianceTest(unittest.TestCase):
    """Run PEP8 on all files in this directory and subdirectories."""

    def _ignore(self, directory: str) -> bool:
        """Should the directory be ignored?"""

        for pattern in ignore_patterns:
            if pattern in directory:
                return True
        return False

    def test_pep8_compliance(self) -> None:
        style = pycodestyle.StyleGuide(quiet=False, ignore="E501")
        errors = 0
        for root, _, files in os.walk(ROOT):
            if self._ignore(root):
                continue
            python_files = [os.path.join(root, f) for f in files if
                            f.endswith('.py')]
            errors += style.check_files(python_files).total_errors

        self.assertEqual(errors, 0, 'PEP8 style errors: {}'.format(errors))
