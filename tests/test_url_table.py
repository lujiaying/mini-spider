from tools import url_table

def test_bloom_filter():
    bf_instance = url_table.BloomFilter()
    bf_instance.init(1000)

    bf_instance.add(1)
    bf_instance.add(2)
    bf_instance.add(66666)

    assert True == (1 in bf_instance)
    assert True == (2 in bf_instance)
    assert True == (66666 in bf_instance)
    assert False == (3 in bf_instance)
    assert False == (66665 in bf_instance)
