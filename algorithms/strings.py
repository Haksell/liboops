def make_lps(s):
    lps = [0] * len(s)
    length = 0
    i = 1
    while i < len(s):
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length == 0:
            i += 1
        else:
            length = lps[length - 1]
    return lps


def test_lps():
    assert make_lps("") == []
    assert make_lps("a") == [0]
    assert make_lps("aa") == [0, 1]
    assert make_lps("aaa") == [0, 1, 2]
    assert make_lps("aaaa") == [0, 1, 2, 3]
    assert make_lps("ab") == [0, 0]
    assert make_lps("aba") == [0, 0, 1]
    assert make_lps("abab") == [0, 0, 1, 2]
    assert make_lps("ababa") == [0, 0, 1, 2, 3]
    assert make_lps("ababab") == [0, 0, 1, 2, 3, 4]
    assert make_lps("abababa") == [0, 0, 1, 2, 3, 4, 5]
    assert make_lps("abababab") == [0, 0, 1, 2, 3, 4, 5, 6]
    assert make_lps("abcababc") == [0, 0, 0, 1, 2, 1, 2, 3]
    assert make_lps("abcdef") == [0, 0, 0, 0, 0, 0]
    assert make_lps("abcabc") == [0, 0, 0, 1, 2, 3]
    assert make_lps("abacaba") == [0, 0, 1, 0, 1, 2, 3]
    assert make_lps("aabaaac") == [0, 1, 0, 1, 2, 2, 0]
    assert make_lps("abcdeabcd") == [0, 0, 0, 0, 0, 1, 2, 3, 4]
    assert make_lps("abacadaeafa") == [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
