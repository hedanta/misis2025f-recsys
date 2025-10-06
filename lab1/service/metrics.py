from typing import List, Dict, Any


def compare_tags(tags1: List[str], tags2: List[str]) -> Dict[str, Any]:
    s1, s2 = set(tags1), set(tags2)
    overlap = s1 & s2

    return {
        "overlap": sorted(overlap),
        "unique_api1": len(s1 - s2),
        "unique_api2": len(s2 - s1),
    }
