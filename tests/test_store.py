import pytest

from bjlab.store import InMemoryStore, JsonStore


def test_in_memory_roundtrip():
    s = InMemoryStore()
    assert s.get("k") is None
    s.put("k", {"a": 1})
    assert s.get("k") == {"a": 1}


def test_get_or_compute_computes_once():
    s = InMemoryStore()
    calls = []

    def compute():
        calls.append(1)
        return [1, 2, 3]

    assert s.get_or_compute("k", compute) == [1, 2, 3]
    assert s.get_or_compute("k", compute) == [1, 2, 3]
    assert len(calls) == 1


def test_none_is_not_storable():
    with pytest.raises(ValueError):
        InMemoryStore().put("k", None)


def test_json_store_roundtrip(tmp_path):
    s = JsonStore(tmp_path)
    assert s.get("missing") is None
    s.put("strategy/basic:abc123", {"table": {"hard,16,10": "HIT"}})
    assert s.get("strategy/basic:abc123") == {"table": {"hard,16,10": "HIT"}}


def test_json_store_persists_across_instances(tmp_path):
    JsonStore(tmp_path).put("k:with/odd\\chars", 42)
    assert JsonStore(tmp_path).get("k:with/odd\\chars") == 42


def test_json_store_get_or_compute(tmp_path):
    s = JsonStore(tmp_path)
    assert s.get_or_compute("k", lambda: "v") == "v"
    assert s.get_or_compute("k", lambda: pytest.fail("should not recompute")) == "v"
