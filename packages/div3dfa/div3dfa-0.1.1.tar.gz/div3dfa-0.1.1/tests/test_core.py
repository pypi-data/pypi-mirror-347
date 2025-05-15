from div3dfa import accepts_binary_string

import pytest
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src/')))

def test_empty_string():
    assert accepts_binary_string("") == True  # 0 ones divisible by 3

def test_divisible_by_3():
    assert accepts_binary_string("111") == True
    assert accepts_binary_string("110110") == False
    assert accepts_binary_string("000") == True  # zero ones

def test_not_divisible_by_3():
    assert accepts_binary_string("1") == False
    assert accepts_binary_string("11011") == False

def test_invalid_characters():
    with pytest.raises(ValueError):
        accepts_binary_string("102")
    with pytest.raises(ValueError):
        accepts_binary_string("abc")
        

