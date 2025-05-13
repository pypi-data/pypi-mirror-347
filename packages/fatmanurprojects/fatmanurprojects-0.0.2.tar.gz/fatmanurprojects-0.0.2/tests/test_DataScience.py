import sys
sys.path.append(".")

import pytest
from src.pythonProject import DataScience

def test_mean():
    assert DataScience.mean([1, 2, 3, 4, 5]) == 3

