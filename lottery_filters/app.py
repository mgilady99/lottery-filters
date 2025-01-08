from flask import Flask, render_template, jsonify, request
from filters import get_combinations, generate_random_sets

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=8080)
