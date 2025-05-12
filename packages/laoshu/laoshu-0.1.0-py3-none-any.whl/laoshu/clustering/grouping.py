from typing import List, Callable, Dict, TypeVar

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def group_by(
    data: List[T], key: Callable[[T], K], value: Callable[[T], V]
) -> Dict[K, List[V]]:
    return {
        k: [value(item) for item in data if key(item) == k]
        for k in set(key(item) for item in data)
    }
