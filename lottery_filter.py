from flask import Flask, render_template, request, jsonify
import math
import random
from itertools import combinations

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
    """Calculate the total number of possible combinations."""
    return math.comb(n, r)

def has_consecutive_numbers(numbers, min_consecutive=3):
    """Check if a set has consecutive numbers."""
    sorted_numbers = sorted(numbers)
    consecutive_count = 1
    for i in range(1, len(sorted_numbers)):
        if sorted_numbers[i] == sorted_numbers[i-1] + 1:
            consecutive_count += 1
            if consecutive_count >= min_consecutive:
                return True
        else:
            consecutive_count = 1
    return False

def count_even_numbers(numbers):
    """Count the number of even numbers in a set."""
    return sum(1 for num in numbers if num % 2 == 0)

def generate_combinations(n, r, start_idx, end_idx):
    """Generate combinations for a specific page."""
    from itertools import combinations
    import itertools
    
    total = calculate_combinations(n, r)
    
    if total > 1000000:  # If more than 1 million combinations
        # Generate only the combinations we need for the current page
        all_numbers = range(1, n + 1)
        combinations_data = []
        
        # Skip combinations until start_idx
        combo_iter = itertools.combinations(all_numbers, r)
        for _ in range(start_idx):
            next(combo_iter, None)
        
        # Take only what we need for this page
        count = 0
        while count < (end_idx - start_idx):
            try:
                combo = next(combo_iter)
                combinations_data.append({
                    'numbers': list(combo),
                    'sum': sum(combo)
                })
                count += 1
            except StopIteration:
                break
    else:
        # For smaller sets, generate all combinations and slice
        all_numbers = range(1, n + 1)
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

def generate_random_set(total_numbers, numbers_to_pick, filter_three_even=False, filter_three_consecutive=False):
    """Generate a random set of numbers with optional filters."""
    max_attempts = 1000  # Prevent infinite loops
    attempts = 0
    
    while attempts < max_attempts:
        numbers = sorted(random.sample(range(1, total_numbers + 1), numbers_to_pick))
        even_count = count_even_numbers(numbers)
        has_three_consecutive = has_consecutive_numbers(numbers, 3)
        
        # Check if the set meets the filter criteria
        if filter_three_even and even_count != 3:
            attempts += 1
            continue
        
        if filter_three_consecutive and has_three_consecutive:
            attempts += 1
            continue
        
        return {
            'numbers': numbers,
            'sum': sum(numbers),
            'even_count': even_count,
            'has_consecutive': has_consecutive_numbers(numbers, 2),
            'has_three_consecutive': has_three_consecutive
        }
    
    return None  # Return None if no valid set found after max attempts

@app.route('/')
def home():
    saved_games = get_saved_games()
    return render_template('index.html', saved_games=saved_games)

@app.route('/combinations', methods=['POST'])
def get_combinations():
    data = request.get_json()
    total_numbers = int(data.get('totalNumbers', 37))  # Default to 37
    numbers_to_pick = int(data.get('numbersToPick', 6))  # Default to 6
    page = int(data.get('page', 1))
    
    if total_numbers < numbers_to_pick:
        return jsonify({'error': 'Total numbers must be greater than numbers to pick'})
    
    total = calculate_combinations(total_numbers, numbers_to_pick)
    if total > 10000000:  # 10 million limit
        return jsonify({'error': f'Too many combinations ({total:,}). Please reduce the numbers.'})
    
    # Calculate pagination
    per_page = 1000
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    try:
        result = generate_combinations(total_numbers, numbers_to_pick, start_idx, end_idx)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error generating combinations: {str(e)}")
        return jsonify({'error': 'Error generating combinations'}), 500

@app.route('/random-sets', methods=['POST'])
def get_random_sets():
    data = request.get_json()
    total_numbers = int(data.get('totalNumbers', 37))  # Default to 37
    numbers_to_pick = int(data.get('numbersToPick', 6))  # Default to 6
    num_sets = int(data.get('numSets', 1))
    filter_three_even = data.get('filterThreeEven', False)
    filter_three_consecutive = data.get('filterThreeConsecutive', False)
    
    if total_numbers < numbers_to_pick:
        return jsonify({'error': 'Total numbers must be greater than numbers to pick'})
    
    if num_sets < 1 or num_sets > 1000:
        return jsonify({'error': 'Number of sets must be between 1 and 1000'})
    
    random_sets = []
    failed_generations = 0
    
    # Generate random sets
    while len(random_sets) < num_sets and failed_generations < num_sets * 2:
        random_set = generate_random_set(
            total_numbers, 
            numbers_to_pick,
            filter_three_even,
            filter_three_consecutive
        )
        
        if random_set:
            random_sets.append(random_set)
        else:
            failed_generations += 1
    
    if len(random_sets) < num_sets:
        return jsonify({
            'error': 'Could not generate enough valid sets with the given filters. Try relaxing the constraints.'
        })
    
    # Calculate statistics
    sums = [s['sum'] for s in random_sets]
    even_counts = [s['even_count'] for s in random_sets]
    consecutive_counts = sum(1 for s in random_sets if s['has_consecutive'])
    three_consecutive_counts = sum(1 for s in random_sets if s['has_three_consecutive'])
    
    stats = {
        'total_sets': len(random_sets),
        'avg_sum': sum(sums) / len(sums),
        'min_sum': min(sums),
        'max_sum': max(sums),
        'consecutive_count': consecutive_counts,
        'three_consecutive_count': three_consecutive_counts,
        'avg_even_count': sum(even_counts) / len(even_counts)
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
    app.run(debug=True, port=8080)
