from IndexMinPQ import IndexMinPQ


def main():
    # construct priority queue
    pq = IndexMinPQ(50)
    # run tests
    test_insert()
    test_min()
    test_change_delete()


def test_insert():
    pq = IndexMinPQ(50)
    # ensure empty
    assert pq.empty()
    assert len(pq) == 0
    # insert
    pq.insert(0, 30)
    pq.insert(1, 10)
    assert len(pq) == 2
    pq.insert(2, 20)
    pq.insert(6, 15)
    assert len(pq) == 4
    # contains
    assert pq.contains(0)
    assert pq.contains(2)
    assert pq.contains(6)
    assert not pq.contains(3)


def test_min():
    pq = IndexMinPQ(50)
    # insert
    pq.insert(0, 30)
    pq.insert(1, 10)
    pq.insert(2, 20)
    pq.insert(6, 15)
    # test min functions
    assert len(pq) == 4
    assert pq.min_index() == 1
    assert pq.min_key() == 10
    assert pq.del_min() == 1
    assert pq.del_min() == 6
    assert len(pq) == 2


def test_change_delete():
    pq = IndexMinPQ(50)
    # insert
    pq.insert(0, 30)
    pq.insert(1, 10)
    pq.insert(2, 20)
    pq.insert(6, 15)
    # test change and delete functions
    assert pq.min_index() == 1
    assert pq.min_key() == 10
    pq.change_key(1, 40)
    assert pq.min_index() == 6
    assert pq.min_key() == 15
    pq.delete(6)
    assert pq.min_index() == 2
    assert pq.min_key() == 20


if __name__ == "__main__":
    main()
