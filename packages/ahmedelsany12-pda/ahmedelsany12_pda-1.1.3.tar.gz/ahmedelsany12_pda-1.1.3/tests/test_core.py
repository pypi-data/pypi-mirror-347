from src.pda_anbn import is_anbn

def test_is_anbn():
    assert is_anbn("ab")
    assert is_anbn("aabb")
    assert is_anbn("aaabbb")
    assert not is_anbn("aabbb")
    assert not is_anbn("abb")
    assert not is_anbn("ba")
    assert is_anbn("")  
