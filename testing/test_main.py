import main
def test_get_none():
    assert main.get_none() == None


def test_flatten_dict():
    assert type(main.flatten_dict({'a': [{'inner_inner_a': 42}]})) == list
    assert main.flatten_dict({'a': 42, 'b': 3.14}) == [42, 3.14]
    assert main.flatten_dict({'a': {'inner_a': 42, 'inner_b': [{ 'd':350, 'g': [20, 30]}]}, 'b': 3.14}) == [42, 350, 20, 30, 3.14]



