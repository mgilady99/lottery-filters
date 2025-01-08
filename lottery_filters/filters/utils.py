def has_consecutive_numbers(numbers, min_consecutive=2):
    """Check if a set has consecutive numbers."""
    sorted_nums = sorted(numbers)
    consecutive_count = 1
    max_consecutive = 1
    
    for i in range(1, len(sorted_nums)):
        if sorted_nums[i] == sorted_nums[i-1] + 1:
            consecutive_count += 1
            max_consecutive = max(max_consecutive, consecutive_count)
        else:
            consecutive_count = 1
    
    return max_consecutive >= min_consecutive, max_consecutive >= 3

def count_even_numbers(numbers):
    """Count the number of even numbers in a set."""
    return sum(1 for num in numbers if num % 2 == 0)
