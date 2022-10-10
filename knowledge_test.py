import pytest
from knowledge import Knowledge

def test_merge():
    k1 = Knowledge({1 : 2})
    k2 = Knowledge({2 : 3, 1:1})

    assert k1.merge(k2).past_rec == {1:1, 2:3}