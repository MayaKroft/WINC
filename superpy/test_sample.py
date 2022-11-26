import doc_handler
import datetime
import main
import getdate
from cli_test_helpers import ArgvContext, shell
import pytest

def test_yesterday():
    assert isinstance(getdate.yesterday(), datetime.date), f'datetime.date object expected, got {type(getdate.yesterday())}'

def test_runas_module():
    """
    Can this package be run as a Python module?
    """
    result = shell('python -m main --help')
    assert result.exit_code == 0


