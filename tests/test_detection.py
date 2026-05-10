import sys
import types

import pytest

# pybgpstream is only available inside the Docker image; stub it so the module
# can be imported in a plain Python environment for testing.
sys.modules.setdefault("pybgpstream", types.ModuleType("pybgpstream"))

from pybgpstream_print import _check_elem  # noqa: E402


def _elem(fields):
    """Build a minimal BGPElem-like object with the given fields dict."""
    return types.SimpleNamespace(fields=fields)


def _withdrawal():
    """Withdrawal records have no .fields attribute."""
    return types.SimpleNamespace()


AUTH_AS = ["62371"]
PREFIX = "185.70.40.0/24"


def test_authorized_as_is_not_flagged():
    elem = _elem({"prefix": PREFIX, "as-path": "1299 3356 62371"})
    pref, aspath, asorin, is_hijack = _check_elem(elem, AUTH_AS)
    assert pref == PREFIX
    assert asorin == "62371"
    assert not is_hijack


def test_unauthorized_as_is_flagged():
    elem = _elem({"prefix": PREFIX, "as-path": "1299 3356 1221"})
    _, _, asorin, is_hijack = _check_elem(elem, AUTH_AS)
    assert asorin == "1221"
    assert is_hijack


def test_multiple_authorized_as_none_flagged():
    elem = _elem({"prefix": PREFIX, "as-path": "1299 99999"})
    _, _, asorin, is_hijack = _check_elem(elem, ["62371", "99999"])
    assert not is_hijack


def test_withdrawal_raises_attribute_error():
    # generate_streams catches AttributeError; verify _check_elem raises it
    with pytest.raises(AttributeError):
        _check_elem(_withdrawal(), AUTH_AS)


def test_missing_as_path_raises_key_error():
    # generate_streams catches KeyError; verify _check_elem raises it
    elem = _elem({"prefix": PREFIX})
    with pytest.raises(KeyError):
        _check_elem(elem, AUTH_AS)
