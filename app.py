from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import itertools
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filters', methods=['POST'])
def apply_filters():
    try:
        data = request.get_json()
        filter_type = data.get('type')
        
        if filter_type == 'base':
            total_numbers = data.get('totalNumbers', 37)
            draw_size = data.get('drawSize', 6)
            combinations = list(itertools.combinations(range(1, total_numbers + 1), draw_size))
            combinations = [list(combo) for combo in combinations]
            return jsonify({'combinations': combinations[:1000]})  # Limit to 1000 combinations
            
        previous_combinations = data.get('previousCombinations', [])
        if not previous_combinations:
            return jsonify({'error': 'No combinations to filter'})

        if filter_type == 'odd_even':
            min_odd = data.get('minOdd')
            max_odd = data.get('maxOdd')
            filtered = []
            for combo in previous_combinations:
                odd_count = sum(1 for num in combo if num % 2 != 0)
                if (min_odd is None or odd_count >= min_odd) and (max_odd is None or odd_count <= max_odd):
                    filtered.append(combo)
            return jsonify({'combinations': filtered})

        elif filter_type == 'distance':
            min_distance = data.get('minDistance')
            max_distance = data.get('maxDistance')
            filtered = []
            for combo in previous_combinations:
                sorted_combo = sorted(combo)
                distances = [sorted_combo[i+1] - sorted_combo[i] for i in range(len(sorted_combo)-1)]
                min_dist = min(distances)
                max_dist = max(distances)
                if (min_distance is None or min_dist >= min_distance) and (max_distance is None or max_dist <= max_distance):
                    filtered.append(combo)
            return jsonify({'combinations': filtered})

        elif filter_type == 'sum':
            sum_min = data.get('sumMin')
            sum_max = data.get('sumMax')
            filtered = []
            for combo in previous_combinations:
                combo_sum = sum(combo)
                if (sum_min is None or combo_sum >= sum_min) and (sum_max is None or combo_sum <= sum_max):
                    filtered.append(combo)
            return jsonify({'combinations': filtered})

        elif filter_type == 'include':
            numbers = data.get('numbers', [])
            filtered = [combo for combo in previous_combinations if all(num in combo for num in numbers)]
            return jsonify({'combinations': filtered})

        elif filter_type == 'exclude':
            numbers = data.get('numbers', [])
            filtered = [combo for combo in previous_combinations if not any(num in combo for num in numbers)]
            return jsonify({'combinations': filtered})

        elif filter_type == 'random':
            count = min(data.get('count', 10), len(previous_combinations))
            filtered = random.sample(previous_combinations, count)
            return jsonify({'combinations': filtered})

        return jsonify({'error': 'Invalid filter type'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
