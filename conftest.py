import pytest  # noqa: F401


def pytest_itemcollected(item):
    if item.obj.__doc__:
        docstring = " ".join(item.obj.__doc__.strip().split())

        item._nodeid = f"{item.nodeid.split('::')[0]} - {docstring}"
