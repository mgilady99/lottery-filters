from flask import Flask, render_template, jsonify, request
import itertools
import random
import math

app = Flask(__name__)

def get_combinations(total_numbers, numbers_to_pick, page=1, per_page=1000):
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

def has_consecutive_numbers(numbers, min_consecutive=2):
    consecutive_count = 1
    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i-1] + 1:
            consecutive_count += 1
            if consecutive_count >= min_consecutive:
                return True
        else:
            consecutive_count = 1
    return False

def count_even_numbers(numbers):
    return sum(1 for num in numbers if num % 2 == 0)

def generate_random_sets(total_numbers, numbers_to_pick, num_sets, filter_three_even=False, filter_three_consecutive=False):
    numbers = list(range(1, total_numbers + 1))
    random_sets = []
    stats = {
        "total_sets": 0,
        "consecutive_count": 0,
        "three_consecutive_count": 0,
        "total_sum": 0,
        "min_sum": float('inf'),
        "max_sum": 0,
        "total_even_count": 0
    }
    
    while len(random_sets) < num_sets:
        combo = sorted(random.sample(numbers, numbers_to_pick))
        combo_sum = sum(combo)
        even_count = count_even_numbers(combo)
        has_consecutive = has_consecutive_numbers(combo, 2)
        has_three_consecutive = has_consecutive_numbers(combo, 3)
        
        # Apply filters
        if filter_three_even and even_count != 3:
            continue
        if filter_three_consecutive and has_three_consecutive:
            continue
        
        random_sets.append({
            "numbers": combo,
            "sum": combo_sum,
            "even_count": even_count,
            "has_consecutive": has_consecutive,
            "has_three_consecutive": has_three_consecutive
        })
        
        # Update statistics
        stats["total_sets"] += 1
        stats["consecutive_count"] += 1 if has_consecutive else 0
        stats["three_consecutive_count"] += 1 if has_three_consecutive else 0
        stats["total_sum"] += combo_sum
        stats["min_sum"] = min(stats["min_sum"], combo_sum)
        stats["max_sum"] = max(stats["max_sum"], combo_sum)
        stats["total_even_count"] += even_count
    
    # Calculate averages
    stats["avg_sum"] = stats["total_sum"] / stats["total_sets"]
    stats["avg_even_count"] = stats["total_even_count"] / stats["total_sets"]
    
    return {
        "random_sets": random_sets,
        "stats": stats
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/combinations', methods=['POST'])
def get_filtered_combinations():
    data = request.get_json()
    total_numbers = data.get('totalNumbers', 37)
    numbers_to_pick = data.get('numbersToPick', 6)
    page = data.get('page', 1)
    
    if total_numbers < numbers_to_pick:
        return jsonify({"error": "Total numbers must be greater than numbers to pick"})
    
    try:
        result = get_combinations(total_numbers, numbers_to_pick, page)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/random-sets', methods=['POST'])
def generate_random():
    data = request.get_json()
    total_numbers = data.get('totalNumbers', 37)
    numbers_to_pick = data.get('numbersToPick', 6)
    num_sets = data.get('numSets', 5)
    filter_three_even = data.get('filterThreeEven', False)
    filter_three_consecutive = data.get('filterThreeConsecutive', False)
    
    if total_numbers < numbers_to_pick:
        return jsonify({"error": "Total numbers must be greater than numbers to pick"})
    
    if num_sets <= 0 or num_sets > 1000:
        return jsonify({"error": "Number of sets must be between 1 and 1000"})
    
    try:
        result = generate_random_sets(
            total_numbers, 
            numbers_to_pick, 
            num_sets,
            filter_three_even,
            filter_three_consecutive
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
