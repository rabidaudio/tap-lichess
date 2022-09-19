"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_lichess.tap import TapLichess

SAMPLE_CONFIG = {"usernames": ["VincentKeymer2004"]}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapLichess, config=SAMPLE_CONFIG)
    # import pdb; pdb.set_trace()
    for test in tests:
        test()
