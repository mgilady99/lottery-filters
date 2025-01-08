from flask import Flask, render_template, jsonify, request
import math
import random
import os
import json

app = Flask(__name__)

# Create directory for saved games if it doesn't exist
SAVES_DIR = os.path.join(os.path.dirname(__file__), 'saves')
os.makedirs(SAVES_DIR, exist_ok=True)

def get_saved_games():
    """Get list of saved game configurations."""
    if not os.path.exists(SAVES_DIR):
        return []
    files = os.listdir(SAVES_DIR)
    return [f.replace('.json', '') for f in files if f.endswith('.json')]

def calculate_combinations(n, r):
    """Calculate total number of combinations."""
    return math.comb(n, r)

def generate_combinations(n, r, start_idx, end_idx):
    """Generate combinations for a specific page."""
    from itertools import combinations
    all_numbers = range(1, n + 1)
    total = calculate_combinations(n, r)
    
    # Generate all combinations and slice for pagination
    all_combinations = list(combinations(all_numbers, r))
    page_combinations = all_combinations[start_idx:end_idx]
    
    combinations_data = []
    for combo in page_combinations:
        combinations_data.append({
            'numbers': list(combo),
            'sum': sum(combo)
        })
    
    return {
        'combinations': combinations_data,
        'total_combinations': total,
        'total_pages': math.ceil(total / 1000)
    }

def has_consecutive_numbers(numbers):
    """Check if numbers contain consecutive values."""
    sorted_nums = sorted(numbers)
    for i in range(len(sorted_nums) - 1):
        if sorted_nums[i + 1] - sorted_nums[i] == 1:
            return True
    return False

def has_three_consecutive_numbers(numbers):
    """Check if numbers contain 3 or more consecutive values."""
    sorted_nums = sorted(numbers)
    consecutive_count = 1
    for i in range(len(sorted_nums) - 1):
        if sorted_nums[i + 1] - sorted_nums[i] == 1:
            consecutive_count += 1
            if consecutive_count >= 3:
                return True
        else:
            consecutive_count = 1
    return False

def count_even_numbers(numbers):
    """Count even numbers in the set."""
    return sum(1 for n in numbers if n % 2 == 0)

def generate_random_sets(n, r, num_sets, filter_three_even=False, filter_three_consecutive=False):
    """Generate random sets of combinations with statistical filters."""
    if num_sets <= 0:
        return []
    
    random_sets = []
    numbers = list(range(1, n + 1))
    attempts = 0
    max_attempts = num_sets * 100  # Prevent infinite loop
    
    while len(random_sets) < num_sets and attempts < max_attempts:
        combo = sorted(random.sample(numbers, r))
        even_count = count_even_numbers(combo)
        has_consecutive = has_consecutive_numbers(combo)
        has_three_consecutive = has_three_consecutive_numbers(combo)
        
        # Apply filters based on user preferences
        if filter_three_even and even_count != 3:
            attempts += 1
            continue
            
        if filter_three_consecutive and has_three_consecutive:
            attempts += 1
            continue
        
        random_sets.append({
            'numbers': combo,
            'sum': sum(combo),
            'even_count': even_count,
            'has_consecutive': has_consecutive,
            'has_three_consecutive': has_three_consecutive
        })
        
        attempts += 1
    
    return random_sets

@app.route('/')
def home():
    saved_games = get_saved_games()
    return render_template('index.html', saved_games=saved_games)

@app.route('/combinations', methods=['POST'])
def get_combinations():
    data = request.get_json()
    total_numbers = int(data.get('totalNumbers', 37))
    numbers_to_pick = int(data.get('numbersToPick', 6))
    page = int(data.get('page', 1))
    
    if total_numbers < numbers_to_pick:
        return jsonify({'error': 'Total numbers must be greater than numbers to pick'})
    
    # Calculate pagination
    per_page = 1000
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    return jsonify(generate_combinations(total_numbers, numbers_to_pick, start_idx, end_idx))

@app.route('/stats', methods=['POST'])
def get_stats():
    data = request.get_json()
    total_numbers = int(data.get('totalNumbers', 37))
    numbers_to_pick = int(data.get('numbersToPick', 6))
    
    stats = calculate_combination_stats(total_numbers, numbers_to_pick)
    return jsonify(stats)

@app.route('/random-sets', methods=['POST'])
def get_random_sets():
    data = request.get_json()
    total_numbers = int(data.get('totalNumbers', 37))
    numbers_to_pick = int(data.get('numbersToPick', 6))
    num_sets = int(data.get('numSets', 1))
    filter_three_even = data.get('filterThreeEven', False)
    filter_three_consecutive = data.get('filterThreeConsecutive', False)
    
    if num_sets > 1000:  # Limit maximum number of random sets
        return jsonify({'error': 'Maximum 1000 random sets allowed'})
    
    random_sets = generate_random_sets(
        total_numbers, 
        numbers_to_pick, 
        num_sets,
        filter_three_even,
        filter_three_consecutive
    )
    
    # Calculate statistics for the random sets
    stats = {
        'total_sets': len(random_sets),
        'avg_sum': sum(s['sum'] for s in random_sets) / len(random_sets) if random_sets else 0,
        'min_sum': min((s['sum'] for s in random_sets), default=0),
        'max_sum': max((s['sum'] for s in random_sets), default=0),
        'consecutive_count': sum(1 for s in random_sets if s['has_consecutive']),
        'three_consecutive_count': sum(1 for s in random_sets if s['has_three_consecutive']),
        'avg_even_count': sum(s['even_count'] for s in random_sets) / len(random_sets) if random_sets else 0
    }
    
    return jsonify({
        'random_sets': random_sets,
        'stats': stats
    })

@app.route('/save', methods=['POST'])
def save_game():
    data = request.get_json()
    game_name = data.get('name')
    if not game_name:
        return jsonify({'error': 'Game name is required'})
    
    filename = os.path.join(SAVES_DIR, f"{game_name}.json")
    with open(filename, 'w') as f:
        json.dump(data, f)
    
    return jsonify({'message': 'Game saved successfully'})

@app.route('/load/<game_name>', methods=['GET'])
def load_game(game_name):
    filename = os.path.join(SAVES_DIR, f"{game_name}.json")
    if not os.path.exists(filename):
        return jsonify({'error': 'Game not found'})
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
