from utils import slugify

def test_slugify():
    assert slugify("Hello World") == "hello-world"
    assert slugify("Test") == "test"
    assert slugify("A B C") == "a-b-c"
    assert slugify("Arrays and Hashing") == "arrays-and-hashing"
    assert slugify("Two Sum") == "two-sum"
    assert slugify("") == ""
