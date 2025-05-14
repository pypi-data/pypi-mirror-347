import unittest
from inspect import signature

from normedtuple.core import normedtuple


# Example norm function
def example_norm(cls, x, y=0):
    """Normalize to tuple of (x, y)."""
    return (x * 2, y + 1)


# Decorate with normedtuple
ExampleTuple = normedtuple(example_norm)


class TestNormedTuple(unittest.TestCase):
    def test_instance_is_tuple(self):
        obj = ExampleTuple(2, 3)
        self.assertIsInstance(obj, tuple)
        self.assertEqual(obj, (4, 4))

    def test_docstring_and_name(self):
        self.assertEqual(ExampleTuple.__doc__, example_norm.__doc__)
        self.assertEqual(ExampleTuple.__name__, example_norm.__name__)

    def test_default_argument(self):
        obj = ExampleTuple(5)
        self.assertEqual(obj, (10, 1))

    def test_signature_preserved(self):
        # Signature exposed on the class constructor (should exclude 'cls')
        expected_public_sig = signature(example_norm).replace(
            parameters=list(signature(example_norm).parameters.values())[1:]
        )
        self.assertEqual(signature(ExampleTuple), expected_public_sig)
        # Signature on __new__ (should match exactly, including 'cls')
        self.assertEqual(signature(ExampleTuple.__new__), signature(example_norm))


if __name__ == "__main__":
    unittest.main()
