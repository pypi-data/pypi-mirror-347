import random
from typing import List, Set

__all__ = [
    "random_first_name",
    "random_last_name",
    "random_full_name",
    "generate_unique_names",
    "generate_unlimited_names"
]

_last_names = [
    "សុខ", "ជា", "ហេង", "ឆៃ", "សាន", "ពិន", "ស៊ន", "លឹម", "អ៊ុន", "តាំង",
    "ម៉ក់", "ខ្លូត", "ទូច", "ឃិន", "យិន", "អេង", "សេង", "សៀង", "សួន", "ជៀង"
]

_first_names = [
    "វិជ្ជា", "ប៊ុនលី", "ស្រីនាង", "ពេជ្រ", "កុសល់", "ទូច", "សុវណ្ណ", "រតនា", "សារិន", "សាន",
    "សម្បត្តិ", "សេរី", "ឆៃហ្វុង", "ជ័យលាស", "វណ្ណៈ", "អភិវឌ្ឍន៍", "សុភមង្គល", "វិមាន", "នគរ", "បុប្ផា"
]

def random_last_name() -> str:
    return random.choice(_last_names)

def random_first_name() -> str:
    return random.choice(_first_names)

def random_full_name() -> str:
    return f"{random_last_name()} {random_first_name()}"

def generate_unique_names(count: int) -> List[str]:
    all_combinations = [f"{ln} {fn}" for ln in _last_names for fn in _first_names]
    max_possible = len(all_combinations)

    if count > max_possible:
        raise ValueError(f"❌ Cannot generate {count} unique names. Max possible: {max_possible}")

    random.shuffle(all_combinations)
    return all_combinations[:count]

def generate_unlimited_names(count: int) -> List[str]:
    seen = set()
    names = []
    attempts = 0

    while len(names) < count:
        name = random_full_name()
        if name not in seen:
            seen.add(name)
            names.append(name)
        else:
            if len(seen) >= len(_last_names) * len(_first_names):
                names.append(name)

        attempts += 1
        if attempts > count * 3:
            break

    return names
