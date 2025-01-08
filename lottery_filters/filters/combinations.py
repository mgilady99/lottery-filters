import itertools
import random
import math
from .utils import has_consecutive_numbers, count_even_numbers

def get_combinations(total_numbers, numbers_to_pick, page=1, per_page=1000):
    """Generate paginated combinations of numbers."""
    numbers = list(range(1, total_numbers + 1))
    all_combinations = list(itertools.combinations(numbers, numbers_to_pick))
    
    total_pages = math.ceil(len(all_combinations) / per_page)
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, len(all_combinations))
    
    page_combinations = []
    for combo in all_combinations[start_idx:end_idx]:
        combo_list = list(combo)
        combo_sum = sum(combo_list)
        page_combinations.append({
            "numbers": combo_list,
            "sum": combo_sum
        })
    
    return {
        "combinations": page_combinations,
        "total_pages": total_pages
    }

def generate_random_sets(total_numbers, numbers_to_pick, num_sets, filter_three_even=False, filter_three_consecutive=False):
    """Generate random sets with optional filters."""
    numbers = list(range(1, total_numbers + 1))
    random_sets = []
    stats = {
        "total_sets": 0,
        "consecutive_count": 0,
        "three_consecutive_count": 0,
        "total_sum": 0,
        "min_sum": float('inf'),
        "max_sum": float('-inf'),
        "total_even": 0
    }
    
    attempts = 0
    max_attempts = num_sets * 10  # Prevent infinite loops
    
    while len(random_sets) < num_sets and attempts < max_attempts:
        attempts += 1
        current_set = sorted(random.sample(numbers, numbers_to_pick))
        current_sum = sum(current_set)
        even_count = count_even_numbers(current_set)
        has_consecutive, has_three_consecutive = has_consecutive_numbers(current_set)
        
        # Apply filters
        if filter_three_even and even_count != 3:
            continue
        if filter_three_consecutive and has_three_consecutive:
            continue
            
        random_sets.append({
            "numbers": current_set,
            "sum": current_sum,
            "even_count": even_count,
            "has_consecutive": has_consecutive,
            "has_three_consecutive": has_three_consecutive
        })
        
        # Update statistics
        stats["total_sets"] += 1
        stats["consecutive_count"] += 1 if has_consecutive else 0
        stats["three_consecutive_count"] += 1 if has_three_consecutive else 0
        stats["total_sum"] += current_sum
        stats["min_sum"] = min(stats["min_sum"], current_sum)
        stats["max_sum"] = max(stats["max_sum"], current_sum)
        stats["total_even"] += even_count
    
    # Calculate averages
    if stats["total_sets"] > 0:
        stats["avg_sum"] = stats["total_sum"] / stats["total_sets"]
        stats["avg_even_count"] = stats["total_even"] / stats["total_sets"]
    else:
        stats["avg_sum"] = 0
        stats["avg_even_count"] = 0
    
    return {
        "random_sets": random_sets,
        "stats": stats
    }
