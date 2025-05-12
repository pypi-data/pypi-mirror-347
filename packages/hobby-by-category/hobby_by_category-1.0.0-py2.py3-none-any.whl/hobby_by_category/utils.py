# hobby_by_category/utils.py
from .data import HOBBY_DATA
import random

def get_all_categories():
    """Returns all hobby categories."""
    return list(HOBBY_DATA.keys())

def get_hobbies_by_category(category: str):
    """Returns hobbies for a given category."""
    return HOBBY_DATA.get(category, [])

def get_random_hobby(category=None):
    """Returns a random hobby (optionally filtered by category)."""
    if category:
        return random.choice(get_hobbies_by_category(category))
    all_hobbies = [hobby for hobbies in HOBBY_DATA.values() for hobby in hobbies]
    return random.choice(all_hobbies)