import pytest

from sapling.constants import PYCUBED_VERSIONS

def pytest_addoption(parser): # TODO add assertion to test cases that checks whether firmware version matches this
    versions_string = ''
    for i, version in enumerate(PYCUBED_VERSIONS):
        versions_string += version
        if i != len(PYCUBED_VERSIONS) - 1:
            versions_string += ' or '
    parser.addoption(
        "--pycubed_version", action="store", default="v5", help=f"version: {versions_string}"
    )

@pytest.fixture
def pycubed_version(request):
    # pytest automatically checks the version
    return request.config.getoption("--pycubed_version")