<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import itertools
import random
import os

app = Flask(__name__)
CORS(app)
=======
from flask import Flask, render_template, request, jsonify, send_from_directory
import itertools
import numpy as np
import json
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

def generate_combinations(total_numbers, draw_size):
    numbers = list(range(1, total_numbers + 1))
    return [list(combo) for combo in itertools.combinations(numbers, draw_size)]

def filter_odd_count(combinations, min_odd=None, max_odd=None):
    if min_odd is None and max_odd is None:
        return combinations
    return [combo for combo in combinations 
            if (min_odd is None or sum(1 for num in combo if num % 2 != 0) >= min_odd) and
               (max_odd is None or sum(1 for num in combo if num % 2 != 0) <= max_odd)]

def filter_distance(combinations, min_dist=None, max_dist=None):
    if min_dist is None and max_dist is None:
        return combinations
    return [combo for combo in combinations 
            if (min_dist is None or (max(combo) - min(combo)) >= min_dist) and
               (max_dist is None or (max(combo) - min(combo)) <= max_dist)]

def filter_sum(combinations, min_sum=None, max_sum=None):
    if min_sum is None and max_sum is None:
        return combinations
    return [combo for combo in combinations 
            if (min_sum is None or sum(combo) >= min_sum) and
               (max_sum is None or sum(combo) <= max_sum)]

def filter_must_include(combinations, numbers):
    if not numbers:
        return combinations
    return [combo for combo in combinations if all(num in combo for num in numbers)]

def filter_must_exclude(combinations, numbers):
    if not numbers:
        return combinations
    return [combo for combo in combinations if not any(num in combo for num in numbers)]

def random_selection(combinations, count):
    if not count or count >= len(combinations):
        return combinations
    return random.sample(combinations, count)
>>>>>>> fb1564456748f3c28f316fd970f3762227d553d9

@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
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
    port = int(os.environ.get('PORT', 10000))
=======
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/filter', methods=['POST'])
def filter_numbers():
    try:
        data = request.get_json()
        action = data.get('action')
        
        if action == 'initial':
            draw_size = int(data.get('drawSize', 0))
            total_numbers = int(data.get('totalNumbers', 0))
            
            if draw_size <= 0 or total_numbers <= 0 or draw_size > total_numbers:
                return jsonify({'error': 'Invalid input parameters'}), 400
                
            combinations = generate_combinations(total_numbers, draw_size)
            return jsonify({
                'combinations': combinations,
                'count': len(combinations)
            })
        
        # Handle individual filters
        combinations = data.get('combinations', [])
        if not combinations:
            return jsonify({'error': 'No combinations provided'}), 400
            
        value = data.get('value', {})
        filtered_combinations = combinations

        if action == 'odd':
            min_odd = int(value.get('min')) if value.get('min') else None
            max_odd = int(value.get('max')) if value.get('max') else None
            filtered_combinations = filter_odd_count(combinations, min_odd, max_odd)
        
        elif action == 'distance':
            min_dist = int(value.get('min')) if value.get('min') else None
            max_dist = int(value.get('max')) if value.get('max') else None
            filtered_combinations = filter_distance(combinations, min_dist, max_dist)
        
        elif action == 'sum':
            min_sum = int(value.get('min')) if value.get('min') else None
            max_sum = int(value.get('max')) if value.get('max') else None
            filtered_combinations = filter_sum(combinations, min_sum, max_sum)
        
        elif action == 'include':
            numbers = [int(x.strip()) for x in value.split(',') if x.strip()] if value else []
            filtered_combinations = filter_must_include(combinations, numbers)
        
        elif action == 'exclude':
            numbers = [int(x.strip()) for x in value.split(',') if x.strip()] if value else []
            filtered_combinations = filter_must_exclude(combinations, numbers)
        
        elif action == 'random':
            count = int(value) if value else None
            filtered_combinations = random_selection(combinations, count)

        return jsonify({
            'combinations': filtered_combinations,
            'count': len(filtered_combinations)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
>>>>>>> fb1564456748f3c28f316fd970f3762227d553d9
    app.run(host='0.0.0.0', port=port)
